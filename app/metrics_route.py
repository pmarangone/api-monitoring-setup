import time
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse
from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, generate_latest

from .metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    REQUEST_SIZE_HISTOGRAM,
    RESPONSE_SIZE_HISTOGRAM,
    update_system_metrics,
)


metrics_router = APIRouter(prefix="/metrics")


@metrics_router.get("")
async def metrics():
    update_system_metrics()
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)


# TODO: measure time added by adding this
async def request_response_size(request, response):
    request_size = int(request.headers.get("content-length", 0))
    REQUEST_SIZE_HISTOGRAM.observe(request_size)
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    response_size = len(response_body)
    response = StreamingResponse(
        iter([response_body]),
        status_code=response.status_code,
        headers=dict(response.headers),
    )
    RESPONSE_SIZE_HISTOGRAM.observe(response_size)

    return response


async def monitor_requests_middleware(request: Request, call_next):
    method = request.method
    path = request.url.path

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)

    if True:
        response = await request_response_size(request, response)

    return response
