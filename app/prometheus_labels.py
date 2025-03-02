from .metrics import REQUEST_DB_DURATION_SECONDS


H_POSTGRES_INSERT_DEVICE = REQUEST_DB_DURATION_SECONDS.labels(
    op="insert", db="postgres", table="fastapi_device"
)
H_POSTGRES_SELECT_DEVICE = REQUEST_DB_DURATION_SECONDS.labels(
    op="select", db="postgres", table="fastapi_device"
)
