run_env:
	uvicorn main:app --reload --env-file=.env

run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

default:
	uvicorn main:app --host 0.0.0.0 --port 5000

build:
	docker build -t interview-app .

dr:
	docker run --gpus all --env-file .env -p 80:80 --name interview-app-container interview-app

exp:
	export $(grep -v '^#' .env | xargs)