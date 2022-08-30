# Run on cron

This repository aims to convert cron notation to be able to run as sleeps in Python.

**NOTE:** At the time there is no functionality for handling combinations of operators yet. For example '\*/2,5 \* \* \* \*' will not work properly.
There is also no functionality for non standard inputs such as '2/5' yet.
The program also cannot take cron input in the forms of 'JAN' or 'MON' for months and days of the week.

The program is dockerized so to specify what file to run and at what cron interval, change the parameters in the Dockerfile.

## Run the program:

```
docker-compose up
```

## Run tests:

```
docker-compose -f docker-compose.test.yml up
```
