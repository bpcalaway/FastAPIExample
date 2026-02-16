#Instruct Podman Engine to use official python:3.12 as the base image
FROM python:3.12

#Create a working directory(app) for the Podman image and container
WORKDIR /app

#Copy the framework and the dependencies of the FastAPI application into the working directory
COPY Pipfile .

#Install the framework and the dependencies in the requirements.txt file in our Podman image and container
RUN python3.12 -m pip install pipenv
RUN pipenv install

#Copy the remaining files and the source code from the host fast-api folder to the FastAPI application container working directory
COPY . .

#Expose the FastAPI application on port 8000 inside the container
EXPOSE 8000

#Start and run the FastAPI application container
CMD ["pipenv", "run", "fastapi", "run"]