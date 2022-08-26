# Run on cron

This repository aims to convert cron notation to be able to run as sleeps in Python.

NOTE: At the time there is no functionality for handling combinations of operators yet. For example '0,1/5 \* \* \* \*' will not work properly.
There is also no functionality for '/' (step values) yet.

To run the program run:

```
python run_on_cron.py <command to run on loop> <cron string>
```

For example:
```
python run_on_cron.py "python test_script.py" "* * * * *"
```
