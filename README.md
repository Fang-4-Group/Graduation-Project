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


### Chatbot
#### Prerequisites
- Create your [LINE Developers Account](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2Fchannel%2Fnew%3Ftype%3Dline-login) and ask me to add you to roles.
- Download [ngrok](https://ngrok.com/download) and register an account to get your auth token.
- Add this official account as a friend.
<div align="center">
  <img src="https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/c369e78a-5553-424e-8ac5-8b0042772d66" width="150" height="150">
</div>

#### Test
```powershell
# Move to chatbot directory
cd .\src\chatbot
```
Add an `.env` file and add the settings below. You can get these variables in LINE Developers Account's Settings.
```env
CHANNEL_SECRET=[YOUR_CHANNEL_SECRET]
CHANNEL_ACCESS_TOKEN=[YOUR_CHANNEL_ACCESS_TOKEN]
```
Upzip the ngrok zip file and add the directory to .\src\chatbot
```python
# Start the server
# Run this command in root
uvicorn src.chatbot.main:app --host localhost --port 8080  --reload
```
The app will run on port 8080.

#### ngrok
execute `ngrok.exe` (It's in the directory you just unzipped)
```powershell
# Set up your ngrok account authentication token
ngrok authtoken [YOUR_AUTH_TOKEN]

# Save your ngrok authentication token
ngrok config add-authtoken [YOUR_AUTH_TOKEN]

# Expose port 8080
ngrok http 8080
```
Copy the Forwarding url value (It is supposed to look like: https://xxxxxx.ngrok-free.app) and send the url to me. I will help you update to Dialog's webhook url.

#### Result expected
If you run the server correctly, the message you get in the chat room will always have "( 我有經過 FastAPI Server )" as a suffix.
<div align="center">
  <img width="260" alt="result" src="https://github.com/Fang-4-Group/Graduation-Project/assets/82760846/80f5899b-8e3b-492e-a6e2-588adff271ee">
</div>


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
