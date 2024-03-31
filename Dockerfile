FROM python:3.6-slim

ENV WORKDIR /srv/KHGT
WORKDIR ${WORKDIR}

#RUN apt-get update && apt-get install -y wget make build-essential libssl-dev zlib1g-dev \
#libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
#libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
#libgdbm-dev libnss3-dev libedit-dev libc6-dev

RUN apt-get update && apt-get install coreutils
COPY ./requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ADD . ${WORKDIR}

CMD ["python", "./labcode_ml10m.py", "--data", "ml10m", "--graphSampleN", "1000", "--save_path", "model_name"]
#CMD ["echo", "123",">abc"]