# TODO: differ between local and prod

import logging
from multiprocessing import Queue
import os

from logging_loki import LokiQueueHandler


def get_logger(name):
    endpoint = os.environ.get("LOKI_ENDPOINT")
    if endpoint is None:
        raise Exception("LOKI_ENDPOINT environment variable is not set")

    environment = os.environ.get("ENV", "PROD")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if environment == "PROD":
        try:
            loki_logs_handler = LokiQueueHandler(
                Queue(-1),
                url=endpoint,
                tags={"application": "fastapi"},
                version="1",
            )

            logger.addHandler(loki_logs_handler)
        except Exception as exc:
            logger.error(f"Error occurred: {exc}")
            raise exc

    return logger
