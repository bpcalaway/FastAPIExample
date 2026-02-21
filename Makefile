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

# TODO we'll need a job to load up and sync the db, there'll be a script for that eventually