import datetime
from pytest import raises
from run_on_cron import weekday_to_cron, check_time_to_execute, cron_time_match, check_cron_input


def test_weekday_to_cron():
    # Sunday
    dt_sun = datetime.datetime(2022, 8, 28)
    assert dt_sun.weekday() == 6
    assert weekday_to_cron(dt_sun.weekday()) == 0

    # Monday
    dt_mon = datetime.datetime(2022, 8, 29)
    assert dt_mon.weekday() == 0
    assert weekday_to_cron(dt_mon.weekday()) == 1

    # Saturday
    dt_sat = datetime.datetime(2022, 8, 27)
    assert dt_sat.weekday() == 5
    assert weekday_to_cron(dt_sat.weekday()) == 6


def test_cron_time_match():
    # Combined input
    with raises(ValueError) as error_info:
        cron_time_match('1-5/2', '1')
    assert str(error_info.value) == "Invalid cron input. Note that the program cannot handle combined inputs such as '1-5/3,50'"

    # Same value
    assert cron_time_match('1', '1')

    # Any value
    assert cron_time_match('*', '33')

    # Range of values
    for i in range(1, 10):
        assert cron_time_match('1-10', str(i))
    for i in range(1, 10):
        assert cron_time_match('11-20', str(i)) == False

    # Step values
    with raises(ValueError) as error_info:
        cron_time_match('1/2', '1')
    assert str(
        error_info.value) == "Non standard cron input. Step values must be specified as '*/x' where x is a value."

    assert cron_time_match('*/2', '24')
    assert cron_time_match('*/2', '3') == False

    # Value list separator
    assert cron_time_match('1-15', '1')
    assert cron_time_match('1-15', '15')
    assert cron_time_match('1-15', '4')
    assert cron_time_match('1-15', '0') == False
    assert cron_time_match('1-15', '16') == False


def test_check_time_to_execute():

    # Every minute
    assert check_time_to_execute(
        ['*', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 23, 0))
    assert check_time_to_execute(
        ['*', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 23, 1)) == False

    # Every hour
    assert check_time_to_execute(
        ['0', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 0, 0))
    assert check_time_to_execute(
        ['0', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 23, 0)) == False

    # Every day
    assert check_time_to_execute(
        ['0', '0', '*', '*', '*'], datetime.datetime(2022, 8, 29, 0, 0, 0))
    assert check_time_to_execute(
        ['0', '0', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 23, 0)) == False

    # Every month
    assert check_time_to_execute(
        ['0', '0', '1', '*', '*'], datetime.datetime(2022, 9, 1, 0, 0, 0))
    assert check_time_to_execute(
        ['0', '0', '1', '*', '*'], datetime.datetime(2022, 8, 29, 11, 23, 0)) == False

    # Every year
    assert check_time_to_execute(
        ['0', '0', '1', '1', '*'], datetime.datetime(2022, 1, 1, 0, 0, 0))
    assert check_time_to_execute(
        ['0', '0', '1', '1', '*'], datetime.datetime(2022, 8, 29, 11, 23, 0)) == False

    # Range of values, minutes 1-12
    assert check_time_to_execute(
        ['1-12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 1, 0))
    assert check_time_to_execute(
        ['1-12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 4, 0))
    assert check_time_to_execute(
        ['1-12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 12, 0))
    assert check_time_to_execute(
        ['1-12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 0, 0)) == False
    assert check_time_to_execute(
        ['1-12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 13, 0)) == False

    # Step values
    assert check_time_to_execute(
        ['1,12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 1, 0))
    assert check_time_to_execute(
        ['1,12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 12, 0))
    assert check_time_to_execute(
        ['1,12,26', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 26, 0))
    assert check_time_to_execute(
        ['1,12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 4, 0)) == False
    assert check_time_to_execute(
        ['1,12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 24, 0)) == False
    assert check_time_to_execute(
        ['1,12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 13, 0)) == False

    # Value list separator
    assert check_time_to_execute(
        ['*/12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 0, 0))
    assert check_time_to_execute(
        ['*/12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 12, 0))
    assert check_time_to_execute(
        ['*/12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 24, 0))
    assert check_time_to_execute(
        ['*/12', '*', '*', '*', '*'], datetime.datetime(2022, 8, 29, 11, 13, 0)) == False

    with raises(ValueError) as error_info:
        check_time_to_execute(['1/12', '*', '*', '*', '*'],
                              datetime.datetime(2022, 8, 29, 11, 13, 0))
    assert str(
        error_info.value) == "Non standard cron input. Step values must be specified as '*/x' where x is a value."


def test_check_cron_input():
    with raises(AssertionError) as error_info:
        check_cron_input('*****')
    assert str(
        error_info.value) == "Invalid cron input, must be five values with space inbetween. For example: '* * * * *'."

    with raises(AssertionError) as error_info:
        check_cron_input('* * * *')
    assert str(
        error_info.value) == "Invalid cron input, must be five values with space inbetween. For example: '* * * * *'."

    with raises(AssertionError) as error_info:
        check_cron_input('* * * * * *')
    assert str(
        error_info.value) == "Invalid cron input, must be five values with space inbetween. For example: '* * * * *'."

    check_cron_input('* * * * *')
