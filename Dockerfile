FROM ubuntu:20.04 AS base_image

WORKDIR /code

RUN apt-get update && apt-get install -y python3-pip

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /code/src

# Run tests
FROM base_image AS test

COPY ./tests /code/tests

CMD ["pytest", "./tests/tests.py"]

FROM base_image AS run-on-cron

COPY docker-entrypoint.sh ./

COPY ./scripts /code/scripts
# COPY example_bash_script.sh ./

ENTRYPOINT ["/code/docker-entrypoint.sh"]