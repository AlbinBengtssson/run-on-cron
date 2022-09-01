FROM ubuntu:20.04 AS base_image

WORKDIR /run-on-cron

RUN apt-get update && apt-get install -y python3-pip

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /run-on-cron/src
COPY ./scripts /run-on-cron/scripts

COPY docker-entrypoint.sh ./

ENTRYPOINT ["/run-on-cron/docker-entrypoint.sh"]