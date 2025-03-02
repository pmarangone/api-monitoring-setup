import time
from functools import wraps
from prometheus_client import Histogram

REQUEST_DB_DURATION_SECONDS = Histogram(
    "db_request_duration_seconds", "Database request duration in seconds", ["operation"]
)


def monitor_db_operation(operation: str):
    """
    Decorator to monitor the database operation duration and track it with Prometheus.
    :param operation: The type of operation (e.g., 'create', 'select')
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                REQUEST_DB_DURATION_SECONDS.labels(operation=operation).observe(
                    duration
                )
                return result
            except Exception as e:
                raise e

        return wrapper

    return decorator
