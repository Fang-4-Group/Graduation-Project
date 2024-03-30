FROM python:3.10.11-bullseye as base

ENV WORKDIR /srv/graduation-project
WORKDIR ${WORKDIR}

RUN apt-get update && apt-get install -y wget unzip
RUN apt-get install -y postgresql postgresql-contrib python3-pymongo \
    && rm -rf /var/lib/apt/lists/*


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

# 啟動 PostgreSQL
EXPOSE 5432

# 切換回使用者 root
USER root

# 安裝 psycopg2 套件
RUN pip install psycopg2

RUN pip install pymongo

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

ADD . ${WORKDIR}
