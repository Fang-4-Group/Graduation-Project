# pgAdmin4 Setup

Follow these steps to configure pgAdmin4 for managing the PostgreSQL database:

## Prerequisite Steps

1. Switch to the master branch of your repository.
2. Update your local repository with changes from remote: `git pull`.
3. Build the Docker images: `docker-compose build` or `make docker-build`.

## Setup and Start

1. Launch the service using Docker Compose: `docker-compose up -d`.
2. Access pgAdmin by navigating to: [http://localhost:5050/login?next=%2F](http://localhost:5050/login?next=%2F).
3. Log in using the credentials provided in the project documentation.
4. Configure the connection to the PostgreSQL database:
    - **General**: Name your connection (e.g., PostgreSQL-gp).
    - **Connection**: Enter the host name (postgres_db), port (5432), and your username (e.g., riceball).
    - Save the configuration.

If you see the database listed in pgAdmin, the setup is successful:
![pgAdmin](https://github.com/Fang-4-Group/Graduation-Project/assets/93365070/da9f4beb-60e0-4e8f-9f6f-9dfc6fb5a31a)
