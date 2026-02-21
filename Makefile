install:
	apt-get update
	apt-get install python3.12 pipenv podman-compose

db:
	podman-compose up -d

db-down:
	podman-compose down

local:
	pipenv install
	pipenv run uvicorn app:app --host 0.0.0.0 --port 8001 --reload