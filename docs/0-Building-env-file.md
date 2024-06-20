# Build `ENV` file

This README provides instructions for creating a customized `.env` file for your project. The `.env` file is essential for defining environment variables that configure various services and settings in your Dockerized environment.

## Instructions

### 1. PostgreSQL Configuration

Set up the environment variables for PostgreSQL:

- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.
- `POSTGRES_DB`: The default database to connect to.
- `POSTGRES_HOST`: The hostname of the PostgreSQL container.
- `POSTGRES_PORT`: The port on which PostgreSQL listens.


### 2. pgAdmin Configuration

Configure pgAdmin with the following variables:

- `PGADMIN_DEFAULT_EMAIL`: The default email address for pgAdmin login.
- `PGADMIN_DEFAULT_PASSWORD`: The password for the pgAdmin account.


### 3. MongoDB Configuration

Define the MongoDB settings:

- `MONGO_HOST`: The hostname of the MongoDB container.
- `MONGO_PORT`: The port on which MongoDB listens.
- `MONGO_DB`: The default database to connect to.
- `MONGO_COLLECTION`: The default collection to use.

### 4. Docker Platform Configuration

Specify the platform based on your OS and architecture:

- `DOCKER_PLATFORM`: The platform for Docker.

For macOS or if running on AMD64 architecture:
```env
DOCKER_PLATFORM="linux/arm64"
```

For Windows OS if running on ARM64 architecture:
```env
DOCKER_PLATFORM="linux/amd64"
```

### 5. LINE Bot Settings

Configure LINE Bot settings:

- `CHANNEL_SECRET`: The channel secret for your LINE Bot.
- `CHANNEL_ACCESS_TOKEN`: The channel access token for your LINE Bot.

### 6. MongoDB URI Configuration

Set up the MongoDB URI and database name for a different service:

- `MONGO_URI`: The URI for connecting to MongoDB.
- `MONGO_DB_NAME`: The database name for your project.
- `MONGO_COLLECTION`: The collection name for storing chat records.

### 7. Google OIDC Login Settings

Configure Google OIDC login settings:

- `GOOGLE_CLIENT_ID`: The client ID for Google OIDC.
- `GOOGLE_CLIENT_SECRET`: The client secret for Google OIDC.
- `GOOGLE_REDIRECT_URI`: The redirect URI for Google OIDC authentication.

### 8. GPU Configuration

Set the GPU settings based on your GPU type:

For Nvidia GPU:
```env
GPU_MODE=nvidia
GPU_RUNTIME=nvidia
```

For AMD GPU:
```env
GPU_MODE=amd
GPU_RUNTIME=runc
```

For no GPU:
```env
GPU_MODE=none
GPU_RUNTIME=runc
```

## Example `.env` File

Here is an [example](../example.env) of a complete `.env` file.

Customize the values based on your specific setup and requirements. Save this file as `.env` in the root directory of your project. This file will be used by Docker and other services to configure the environment accordingly.
