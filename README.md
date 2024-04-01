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

### pgAdmin4 Setting Steps
#### Prerequisite step: 
1. switch to master branch
2. `git pull`
3. Run `docker-compose build` or `make docker-build`
#### Setup and startup steps
1. Deploying the service using Docker Compose
    ```docker-compose up -d```
2. Click the url: http://localhost:5050/login?next=%2F
3. login(see the line notepad)
4. Click **Add New Server**
5. Setting  
    **-General-**  
    Name: PosgreSQL-gp  
    
    **-Connection-**  
    Host Name/Address: postgres_db  
    Port: 5432  
    Username: riceball  
    
    **Click Save**
    
6. If you can see the picture below on the left above sidebar of your window, you made it.  
   <img src="https://github.com/Fang-4-Group/Graduation-Project/assets/93365070/da9f4beb-60e0-4e8f-9f6f-9dfc6fb5a31a" width="230" height="120">
