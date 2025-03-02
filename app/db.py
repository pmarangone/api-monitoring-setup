from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

import asyncpg
from fastapi import Depends, FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


POSTGRES_URI = POSTGRES_URI = os.environ["POSTGRES_URI"]
POSTGRES_POOL_SIZE = int(os.environ["POSTGRES_POOL_SIZE"])


class Database:
    __slots__ = ("_pool",)

    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    @staticmethod
    async def from_postgres() -> Database:
        """Create connection pool if it doesn't exist"""
        try:
            pool = await asyncpg.create_pool(
                POSTGRES_URI,
                min_size=1,
                max_size=POSTGRES_POOL_SIZE,
                max_inactive_connection_lifetime=300,
            )
            logger.info("Database pool created: %s", pool)

            return Database(pool)
        except asyncpg.exceptions.PostgresError as e:
            logging.error(f"Error creating PostgreSQL connection pool: {e}")
            raise ValueError("Failed to create PostgreSQL connection pool")
        except Exception as e:
            logging.error(f"Unexpected error while creating connection pool: {e}")
            raise

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get database connection from pool"""
        async with self._pool.acquire() as connection:
            logger.info("Connection acquired from pool")
            yield connection
            logger.info("Connection released back to pool")

    async def close(self):
        """Close the pool when shutting down"""
        await self._pool.close()
        logger.info("Database pool closed")


db: Database


async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    async with db.get_connection() as conn:
        yield conn


PostgresDep = Annotated[asyncpg.Connection, Depends(get_db)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for database connection"""
    print(" Starting up database connection...")
    try:
        global db
        db = await Database.from_postgres()
        logger.info(" Database pool created successfully")

        yield
    except Exception:
        logger.exception("Failed to create database pool")
        raise
    finally:
        # Shutdown: close all connections
        logger.info(" Shutting down database connection...")
        await db.close()
        logger.info(" Database connections closed")
