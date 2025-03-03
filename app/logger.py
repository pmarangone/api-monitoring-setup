# TODO: differ between local and prod

import logging
from multiprocessing import Queue
import os

from logging_loki import LokiQueueHandler


def get_logger(name):
    environment = os.environ.get("ENV", "PROD")
    logger = None

    if environment == "PROD":
        loki_logs_handler = LokiQueueHandler(
            Queue(-1),
            url=os.environ["LOKI_ENDPOINT"],
            tags={"application": "fastapi"},
            version="1",
        )

        logger = logging.getLogger(name)
        logger.addHandler(loki_logs_handler)

    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.info)

    return logger
