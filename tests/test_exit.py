import sys

import pytest


def test_exit():
    exit()


def test_os_exit():
    sys.exit()


def test_pytest_outcomes_exit():
    try:
        x = 1 / 0
    except Exception as error:
        raise pytest.outcomes.Exit()


def test_pytest_exit():
    try:
        x = 1 / 0
    except Exception as error:
        pytest.exit(msg=", ".join(error.args))


@pytest.mark.gs
def test_pytest_fail():
    try:
        x = 1 / 0
    except Exception as error:
        pytest.fail(msg=", ".join(error.args), pytrace=False)
