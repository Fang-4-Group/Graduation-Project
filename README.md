# Graduation Project
## A Recommendation System and GAI App for Enhancing Co-Living Experiences Between the Young and Elderly

### Installing Docker and Starting the Daemon
Before setting up your development environment, it's essential to have Docker installed on your system as it will be used to build and deploy your application. Follow these steps to install Docker and start the Docker daemon:

Refer to the official Docker documentation for installation instructions tailored to your OS: [Docker Installation](https://www.docker.com/products/docker-desktop/).

### Launching the API Service Locally
Ensure Docker is installed on your machine before proceeding. Here are the commands to build the Docker image, deploy containers, and initiate the API service in your local environment:

```bash
# Building the Docker image using Makefile
make docker-build

# Alternative command if 'make' is unavailable
docker-compose build

# Deploying the service using Docker Compose
docker-compose up -d

# Accessing the container's shell
docker exec -it graduation-project /bin/bash

# Starting the API service with Uvicorn on localhost
uvicorn src.main:app --host localhost --port 7877 --reload
```

### Accessing the Frontend Container
To work directly with the frontend in development, you can access its container similarly:

```bash
# Accessing the frontend container's shell
docker exec -it graduation-project-frontend-1 /bin/bash

# Inside the container, you might start the development server or run other npm scripts:
npm run serve
```

### Setting Up Pre-commit Hooks
To maintain code quality and ensure that changes adhere to best practices, pre-commit hooks are used. Here's how to install and configure them:

```bash
# Installing the pre-commit package
pip install pre-commit

# Configuring pre-commit hooks to run automatically before commits
pre-commit install --install-hooks
```

### Chatbot Setup
#### Prerequisites
Before setting up the chatbot, complete the following prerequisites:
- Create a [LINE Developers Account](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2Fnew%3Ftype%3Dline-login) and request role access.
- Download [ngrok](https://ngrok.com/download), a tool that will expose your local development server to the Internet.
- Add the official LINE account as a friend using the QR code below:
<div align="center">
  <img src="https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/c369e78a-5553-424e-8ac5-8b0042772d66" width="150" height="150">
</div>

#### Configuration
Configure environment settings before running the chatbot service:
```powershell
# Navigate to the chatbot directory
cd .\src\chatbot

# Copy the example.env, rename it to .env, and set the required environment variables:
# These values are found in the LINE Developers Console.
CHANNEL_SECRET=[YOUR_CHANNEL_SECRET]
CHANNEL_ACCESS_TOKEN=[YOUR_CHANNEL_ACCESS_TOKEN]

# Depending on your operating system's architecture, choose the correct build (amd/arm).
```

#### Running the Chatbot
Run the chatbot using the following command in the project root:

```bash
# Start the chatbot service
uvicorn src.chatbot.main:app --host localhost --port 8080 --reload
```

#### ngrok Setup
Expose your local server to the Internet using ngrok:

```powershell
# Execute ngrok
ngrok authtoken [YOUR_AUTH_TOKEN]  # Authenticate your ngrok session
ngrok http 8080  # Expose local port 8080 to the Internet
```

Share the generated ngrok URL (e.g., https://xxxxxx.ngrok-free.app) with the administrator to update the webhook URL for real-time communication.

#### Expected Result
If everything is set up correctly, messages received in the chat room will include the suffix "(我有經過 FastAPI Server)".
<div align="center">
  <img width="260" alt="result" src="https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/80f5899b-8e3b-492e-a6e2-588adff271ee">
</div>

### pgAdmin4 Setup
Follow these steps to configure pgAdmin4 for managing the PostgreSQL database:

#### Prerequisite Steps:
1. Switch to the master branch of your repository.
2. Update your local repository with changes from remote: `git pull`.
3. Build the Docker images: `docker-compose build` or `make docker-build`.

#### Setup and Start:
1. Launch the service using Docker Compose: `docker-compose up -d`.
2. Access pgAdmin by navigating to: [http://localhost:5050/login?next=%2F](http://localhost:5050/login

?next=%2F).
3. Log in using the credentials provided in the project documentation.
4. Configure the connection to the PostgreSQL database:
    - **General**: Name your connection (e.g., PostgreSQL-gp).
    - **Connection**: Enter the host name (postgres_db), port (5432), and your username (e.g., riceball).
    - Save the configuration.

If you see the database listed in pgAdmin, the setup is successful:
   <img src="https://github.com/Fang-4-Group/Graduation-Project/assets/93365070/da9f4beb-60e0-4e8f-9f6f-9dfc6fb5a31a" width="230" height="120">

### MongoDB Extension Setup for Visual Studio Code
Install and configure the MongoDB extension to manage databases directly from VS Code:

#### Installation:
1. Search for "MongoDB" in the Extensions sidebar in VS Code.
2. Install the **MongoDB for VS Code** extension.
3. Restart VS Code to activate the extension.

#### Configuration:
Follow the instructions in this [video tutorial](https://youtu.be/3XkHMh91dtQ?si=CSQwmWVK4FGo0hVJ&t=328) starting at 5:28 to configure your MongoDB connection.
