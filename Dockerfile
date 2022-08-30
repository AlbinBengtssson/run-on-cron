FROM python:3.9 as python_base

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /code/src

# Run tests
FROM python_base AS test

COPY ./tests /code/tests

CMD ["pytest", "./tests/tests.py"]

# Run the desired program
FROM python_base AS run-on-cron

#   <relative path to file to run>   
COPY example_py_script.py ./

#                                          "<command>  <filename>""       "<cron exp>"
CMD ["python", "-u", "src/run_on_cron.py", "python example_py_script.py", "* * * * *"]
