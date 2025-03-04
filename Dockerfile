FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD ["/app/.venv/bin/gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "--timeout", "60", "--graceful-timeout", "60",  "--log-level", "info", "app.main:app",  "--bind", "0.0.0.0:8000"]