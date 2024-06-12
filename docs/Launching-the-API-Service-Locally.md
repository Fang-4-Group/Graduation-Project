# Launching the API Service Locally

Ensure Docker is installed on your machine before proceeding. Here are the commands to build the Docker image, deploy containers, and initiate the API service in your local environment:

```bash
# Building the Docker image using Makefile
make docker-build

# Alternative command if 'make' is unavailable
docker-compose build

# Deploying the service using Docker Compose
docker-compose up -d
# Deploying the service using Docker Compose with the Nvidia GPU settings
docker-compose -f docker-compose.gpu.yml up -d

# Accessing the container's shell
docker exec -it graduation-project /bin/bash

# Starting the API service with Uvicorn on localhost
uvicorn src.main:app --host localhost --port 7877 --reload
```
