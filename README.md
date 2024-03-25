# Graduation Project
## A Recommendation System and GAI App for Enhancing Co-Living Experiences Between the Young and Elderly

### Installing Docker and Starting the Daemon
Before setting up your development environment, it's essential to have Docker installed on your system as it will be used to build and deploy your application. Follow these steps to install Docker and start the Docker daemon.

Please refer to the official Docker documentation for installation instructions tailored to your OS: [Docker](https://www.docker.com/products/docker-desktop/)


### Launching the API Service Locally

The following commands guide you through building the Docker image, deploying containers, and initiating the API service in your local environment. Ensure Docker is installed on your machine before proceeding.

```bash
# Building the Docker image
make docker-build

# If there's no "make" command in your environment
docker-compose build

# Deploying the service using Docker Compose
docker-compose up -d

# Accessing the container's shell
docker exec -it graduation-project /bin/bash

# Starting the API service with Uvicorn
uvicorn src.main:app --host localhost --port 7877 --reload
```

### Setting Up Pre-commit Hooks

To maintain code quality and ensure that changes adhere to best practices, install and configure pre-commit hooks.

```bash
# Installing the pre-commit package
pip install pre-commit

# Configuring pre-commit hooks
pre-commit install --install-hooks
```
