# Use an official Python runtime as a parent image
FROM python:3.10.11-bullseye as base

# Set the working directory
ENV WORKDIR /srv/graduation-project
WORKDIR ${WORKDIR}

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y wget unzip postgresql postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

# Start PostgreSQL service (Note: This won't persist when the container is run)
RUN service postgresql start && \
    mkdir -p /etc/postgresql/14/main && \
    echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/14/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf && \
    service postgresql stop

# Set up Python environment
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Add the rest of the application
ADD . ${WORKDIR}

# Expose port 5432 for PostgreSQL
EXPOSE 5432
