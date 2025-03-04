run_env:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file=.env 

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

up:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

build:
	docker compose build && docker compose up -d

exp:
	export $(grep -v '^#' .env | xargs)