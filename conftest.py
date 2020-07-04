import datetime

import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: ...")


def pytest_collection_modifyitems(config, items):
    def activate_at(day, month, year):
        return datetime.date.today() < datetime.date(year, month, day)

    skip = pytest.mark.skipif(condition=activate_at(14, 4, 2020), reason="wait on bug fix")
    smoke = pytest.mark.smoke
    for index, item in enumerate(items):
        item.add_marker(skip)
        if index % 2 == 0:
            item.add_marker(smoke)
