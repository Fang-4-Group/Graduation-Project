FROM python:3.10.11-bullseye as base

ENV WORKDIR /srv/graduation-project
WORKDIR ${WORKDIR}

RUN apt-get update && apt-get install -y wget unzip

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

ADD . ${WORKDIR}
