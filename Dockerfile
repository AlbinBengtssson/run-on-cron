FROM python:3.9

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /code/src

COPY ./tests /code/tests

CMD ["pytest", "./tests/tests.py"]

