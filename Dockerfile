# Use an official Python runtime as a parent image
FROM python:3.10.11-bullseye as base

# Set the working directory
ENV WORKDIR /srv/graduation-project
WORKDIR ${WORKDIR}

RUN apt-get update && apt-get install -y wget unzip postgresql postgresql-contrib python3-pymongo && rm -rf /var/lib/apt/lists/*

# 啟動 PostgreSQL 服務
RUN service postgresql start

# 配置 PostgreSQL
USER postgres

# 創建目錄以確保路徑存在
RUN mkdir -p /etc/postgresql/14/main

# 修改配置以允許遠程訪問
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/14/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf

# 停止 PostgreSQL 服務
RUN service postgresql stop

# Set up Python environment
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Add the rest of the application
ADD . ${WORKDIR}

# Expose port 5432 for PostgreSQL
EXPOSE 5432
