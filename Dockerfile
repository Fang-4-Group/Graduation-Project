# Use an official Python runtime as a parent image
FROM python:3.10.11-bullseye as base

# Set the working directory
ENV WORKDIR /srv/graduation-project
WORKDIR ${WORKDIR}

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y wget unzip flac && \
    rm -rf /var/lib/apt/lists/*

# Set up Python environment
# Copy and install base dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy and install extra dependencies
COPY ./extra-requirements.txt ./
RUN pip install -r extra-requirements.txt

# Add the rest of the application
ADD . ${WORKDIR}
