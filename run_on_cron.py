from datetime import datetime
from time import sleep
from subprocess import Popen
from sys import argv

'''
Cron Cheat Sheet:

┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
│ │ │ │ ┌───────────── day of the week (0 - 6 or SUN-SAT)
│ │ │ │ │
│ │ │ │ │
│ │ │ │ │
* * * * *

*   :   Any value
,   :   Value list separator
-   :   Range of values
/   :   Step values

Example:
'5 0 * 8 *'
'At 00:05 in August'

'''


def cron_time_match(cron_val, time_val):
    # Checks whether the time_val is within the specification of the cron value.
    # NOTE: This only checks a single value, not a complete cron string.
    # TODO: Handle combined inputs such as '1-5/3,5'.

    match = False

    if cron_val == '*' or cron_val == time_val:
        match = True

    elif '-' in cron_val:
        cron_val_min = int(cron_val.split('-')[0])
        cron_val_max = int(cron_val.split('-')[1])
        if (int(time_val) <= cron_val_max and int(time_val) >= cron_val_min):
            match = True

    elif ',' in cron_val:
        values = cron_val.split(',')
        if time_val in values:
            match = True

    elif '/' in cron_val:
        cron_step_vals = cron_val.split('/')

        if cron_step_vals[0] != '*':
            raise ValueError(
                "Non standard cron input. Step values must be specified as '*/x' where x is a value.")
        if int(time_val) % int(cron_step_vals[1]) == 0:
            match = True

    else:
        raise ValueError(
            "Invalid cron input. Note that the program cannot handle combined inputs such as '1-5/3,50'")

    return match


def weekday_to_cron(datetime_weekday):
    # Converts datetime's (0-6, MON-SUN) to Cron's (0-6, SUN-SAT)

    if datetime_weekday == 6:
        return 0
    else:
        return datetime_weekday + 1


def check_time_to_execute(cron):
    # Checks whether it is time to execute the program according to the cron specification.

    current_time = datetime.now()

    if (cron_time_match(cron[3], str(current_time.month))
            and cron_time_match(cron[4], str(weekday_to_cron(current_time.weekday())))
            and cron_time_match(cron[2], str(current_time.day))
            and cron_time_match(cron[1], str(current_time.hour))
            and cron_time_match(cron[0], str(current_time.minute))
            and current_time.second == 0):
        return True

    return False


# Input:
#       command:    Command that shoudl be ran, for example 'python script.py' or 'bash script.sh'
#       cron:       Cron expression in the form of a string, for example '5 4 * * *'.
if __name__ == "__main__":
    command = argv[1]
    cron = argv[2].split()

    while True:
        if check_time_to_execute(cron):
            print('Executing at: ', datetime.now())
            Popen(command, shell=True, stdout=False)
            sleep(50)

        while datetime.now().second != 0:
            sleep(0.5)
