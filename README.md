# Graduation Project
## A Recommendation System and GAI App for Enhancing Co-Living Experiences Between the Young and Elderly

### Preparing Your Development Environment

To ensure a smooth development process, it's crucial to utilize a virtual environment. This step helps in maintaining a clean workspace by segregating your project's dependencies.

```bash
# Establishing a virtual environment
python3 -m venv myvenv

# Activating the virtual environment
source myvenv/bin/activate
```

### Launching the API Service Locally

The following commands guide you through building the Docker image, deploying containers, and initiating the API service in your local environment. Ensure Docker is installed on your machine before proceeding.

```bash
# Building the Docker image
make docker-build

# Deploying the service using Docker Compose
docker-compose up -d

# Accessing the container's shell
docker exec -it graduation-project /bin/bash

# Starting the API service with Uvicorn
uvicorn src.main:app --host 0.0.0.0 --port 7877 --reload
```

### Setting Up Pre-commit Hooks

To maintain code quality and ensure that changes adhere to best practices, install and configure pre-commit hooks.

```bash
# Installing the pre-commit package
pip install pre-commit

# Configuring pre-commit hooks
pre-commit install --install-hooks
```
