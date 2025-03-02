import time
from fastapi import APIRouter, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest

from .metrics import REQUEST_COUNT, REQUEST_LATENCY, update_system_metrics


metrics_router = APIRouter(prefix="/metrics")


@metrics_router.get("")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)


async def monitor_requests(request: Request, call_next):
    method = request.method
    path = request.url.path

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)

    return response
