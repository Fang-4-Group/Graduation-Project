# Use an official Python runtime as a parent image
FROM python:3.10.11-bullseye as base

# Set the working directory
ENV WORKDIR /srv/graduation-project
WORKDIR ${WORKDIR}

# Install necessary system dependencies
RUN apt-get update
RUN apt-get install -y wget unzip
RUN rm -rf /var/lib/apt/lists/*

# Set up Python environment
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Add the rest of the application
ADD . ${WORKDIR}
