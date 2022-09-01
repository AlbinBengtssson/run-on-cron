# Run on cron

This repository aims to convert cron notation to be able to run as sleeps in Python.

**NOTE:** At the time there is no functionality for handling combinations of operators yet. For example '\*/2,5 \* \* \* \*' will not work properly.
There is also no functionality for non standard inputs such as '2/5' yet.
The program also cannot take cron input in the forms of 'JAN' or 'MON' for months and days of the week.

## Instructions

```
docker run --rm -v $(pwd):/run-on-cron run-on-cron --run=<command> --cron=<cron expression>
```

### Examples

Running a bash command

```
docker run --rm -v $(pwd):/run-on-cron run-on-cron --run="echo 'Hello world!'" --cron="* * * * *"
```

Running a python file

```
docker run --rm -v $(pwd):/run-on-cron run-on-cron --run="python3 scripts/example_py_script.py" --cron="* * * * *"
```
