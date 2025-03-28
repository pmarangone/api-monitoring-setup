import time
import datetime
import uuid

from asyncpg import PostgresError
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse, PlainTextResponse
from pydantic import BaseModel


from .db import PostgresDep, lifespan
from .metrics_route import metrics_router, monitor_requests_middleware
from .repository import repo_create_device, repo_select_device
from .logger import get_logger

app = FastAPI(lifespan=lifespan)

app.include_router(metrics_router)
app.middleware("http")(monitor_requests_middleware)

logger = get_logger(__name__)


@app.get("/healthz", response_class=PlainTextResponse)
def health():
    logger.info(
        "Health",
        extra={"tags": {"service_name": "my-service"}},
    )
    return "OK"


class DeviceRequest(BaseModel):
    mac: str
    firmware: str


@app.post("/api/devices", status_code=201, response_class=ORJSONResponse)
async def create_device(device: DeviceRequest, conn: PostgresDep):
    try:
        logger.info("Creating device")
        now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        device_uuid = uuid.uuid4()

        insert_query = """
            INSERT INTO fastapi_device (uuid, mac, firmware, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
        """

        row = await repo_create_device(
            conn, insert_query, device_uuid, device.mac, device.firmware, now, now
        )

        if not row:
            raise HTTPException(
                status_code=500, detail="Failed to create device record"
            )

        return {
            "id": row["id"],
            "uuid": str(device_uuid),
            "mac": device.mac,
            "firmware": device.firmware,
            "created_at": now,
            "updated_at": now,
        }

    except PostgresError as exc:
        logger.exception(f"Postgres error: {exc}")
        raise HTTPException(
            status_code=500, detail="Database error occurred while creating device"
        )

    except Exception:
        logger.exception("Unknown error")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred while creating device"
        )


@app.get("/api/devices", response_class=ORJSONResponse)
async def get_devices(conn: PostgresDep):
    try:
        logger.info("Selecting devices")
        query = "SELECT id, uuid, mac, firmware, created_at, updated_at FROM fastapi_device;"

        rows = await repo_select_device(conn, query)

        return [
            {
                "id": row["id"],
                "uuid": str(row["uuid"]),
                "mac": row["mac"],
                "firmware": row["firmware"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
            for row in rows
        ]

    except PostgresError as exc:
        logger.exception(f"Postgres error: {exc}")
        raise HTTPException(
            status_code=500, detail="Database error occurred while retrieving devices"
        )

    except Exception:
        logger.exception("Unknown error")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while retrieving devices",
        )


@app.get("/slow", response_class=PlainTextResponse)
async def slow():
    time.sleep(3)

    return "OK"
