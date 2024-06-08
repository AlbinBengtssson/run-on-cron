from datetime import datetime
from subprocess import Popen
from sys import argv
from time import sleep
from typing import List, Tuple

# TODO: Add check for month and day of the week. Now it can only handle input in the form of integers, # noqa: E501
#       not 'JAN' or 'MON', etc.

"""
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

"""


def cron_time_match(cron_val: str, time_val: str) -> bool:
    """
    Checks whether the time_val is within the specification of the cron value.
    NOTE: This only checks a single cron value, not a complete cron string.
    """

    # TODO (Albin): Handle combined inputs such as '1-5/3,5'.

    if (
        ("," in cron_val and "/" in cron_val)
        or ("," in cron_val and "-" in cron_val)
        or ("/" in cron_val and "-" in cron_val)
    ):
        raise ValueError(
            "Invalid cron input. The program cannot handle combined inputs such as '1-5/3,50'"  # noqa:E501
        )

    elif cron_val == "*" or cron_val == time_val:
        return True

    elif "-" in cron_val:
        cron_val_min = int(cron_val.split("-")[0])
        cron_val_max = int(cron_val.split("-")[1])
        if int(time_val) <= cron_val_max and int(time_val) >= cron_val_min:
            return True

    elif "," in cron_val:
        values = cron_val.split(",")
        if time_val in values:
            return True

    elif "/" in cron_val:
        cron_step_vals = cron_val.split("/")

        if cron_step_vals[0] != "*":
            raise ValueError(
                "Non standard cron input. Step values must be specified as '*/x' where x is a value."  # noqa: E501
            )
        if int(time_val) % int(cron_step_vals[1]) == 0:
            return True

    return False


def weekday_to_cron(datetime_weekday: int) -> int:
    """
    Converts datetime's (0-6, MON-SUN) to Cron's (0-6, SUN-SAT)
    """

    if datetime_weekday == 6:
        return 0
    else:
        return datetime_weekday + 1


def validate_cron_input(cron: str) -> None:
    """
    Ensures that the cron input is of the right length and form.
    """
    # TODO (Albin): Validate that it is a valid cron string using regex

    try:
        assert len(cron.split()) == 5
    except AssertionError:
        raise AssertionError(
            "Invalid cron input, must be five values with space inbetween. For example: '* * * * *'."  # noqa: E501
        )


def check_time_to_execute(cron: List[str], time: datetime) -> bool:
    """
    Checks whether it is time to execute the program according to the cron
    specification.
    """

    if (
        cron_time_match(cron[3], str(time.month))
        and cron_time_match(cron[4], str(weekday_to_cron(time.weekday())))
        and cron_time_match(cron[2], str(time.day))
        and cron_time_match(cron[1], str(time.hour))
        and cron_time_match(cron[0], str(time.minute))
        and time.second == 0
    ):
        return True

    return False


def filter_input(args: List[str]) -> Tuple[str, str]:
    command = ""
    cron = ""

    for arg in args:
        if "--cron=" in arg:
            cron = arg.split("=")[1]
        elif "--command=" in arg or "--cmd=" in arg:
            command = arg.split("=")[1]
    return command, cron


# Input:
#       command:    Command that shoudl be ran, for example 'python script.py' or 'bash script.sh' # noqa: E501
#       cron:       Cron expression in the form of a string, for example '5 4 * * *'.
if __name__ == "__main__":
    command, cron = filter_input(argv)

    validate_cron_input(cron)

    print(
        "run_on_cron launched at:",
        datetime.now(),
        "\nwith command:",
        command,
        "\nand cron expression:",
        cron,
    )

    while True:

        if check_time_to_execute(cron.split(), datetime.now()):
            print("Executing:", command, "at:", datetime.now())
            Popen(command, shell=True)
            sleep(50)

        while datetime.now().second != 0:
            sleep(0.5)
