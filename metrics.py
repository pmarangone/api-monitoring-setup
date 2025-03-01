from prometheus_client import Counter, Gauge, Histogram
import psutil

# Exactly the same histogram buckets as in Go.
buckets = (
    0.0001,
    0.0002,
    0.0004,
    0.0005,
    0.0006,
    0.0007,
    0.0008,
    0.0009,
    0.001,
    0.01,
    0.02,
    0.03,
    0.04,
    0.05,
    0.06,
    0.07,
    0.08,
    0.09,
    0.1,
    0.15,
    0.2,
    0.25,
    0.3,
    0.35,
    0.4,
    0.45,
    0.5,
    0.55,
    0.6,
    0.65,
    0.7,
    0.75,
    0.8,
    0.85,
    0.9,
    0.95,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
    4.5,
    5.0,
)

##### Database
REQUEST_DB_DURATION_SECONDS = Histogram(
    "myapp_request_duration_seconds",  # name
    "Duration of the request",  # description
    labelnames=("op", "db", "table"),  # labels
    buckets=buckets,  # buckets
)


##### API
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ("method", "status", "path"),
)

REQUEST_COUNT = Counter(
    "http_request_total", "Total HTTP Requests", labelnames=("method", "status", "path")
)

# System metrics
CPU_USAGE = Gauge("process_cpu_usage", "Current CPU usage in percent")
MEMORY_USAGE = Gauge("process_memory_usage_bytes", "Current memory usage in bytes")


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)
