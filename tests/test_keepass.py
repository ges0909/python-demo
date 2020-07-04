import re
from pathlib import Path

import pytest
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsIntegrityError


@pytest.fixture
def path(request):
    return Path.home() / "Desktop" / "syrocon.kdbx"


@pytest.fixture
def kp(request, path):
    return PyKeePass(path, password="syrocon")


@pytest.fixture
def data_cloud_group(request, kp):
    meps = kp.find_groups(name="meps", first=True)
    data_cloud, *_ = [g for g in meps.subgroups if g.name == "data_cloud"]
    return data_cloud


# -- positive tests


def test_load_database_file(path):
    kp = PyKeePass(path, password="syrocon")
    assert kp is not None


def test_find_group_by_name(kp):
    group = kp.find_groups(name="meps", first=True)
    assert group is not None


def test_find_group_in_subgroups(kp):  # nested groups
    group = kp.find_groups(name="meps", first=True)
    data_cloud_group, *_ = [g for g in group.subgroups if g.name == "data_cloud"]
    assert data_cloud_group is not None


def test_get_entries(data_cloud_group):
    assert len(data_cloud_group.entries) == 2


def test_search_entry(data_cloud_group):
    ssh_dev1_entry, *_ = [e for e in data_cloud_group.entries if e.title == "SSH" and "DEV1" in e.tags]
    assert ssh_dev1_entry.title == "SSH"
    assert ssh_dev1_entry.username == "syrocon"
    assert ssh_dev1_entry.password == "syroconsyrocon"
    # access custom properties
    assert ssh_dev1_entry.custom_properties["host"] == "1.2.3.4"


# !KEEPASS group=meps/data_cloud title=SSH tag=DEV1 entry=username
# !KEEPASS group=meps/data_cloud title=SSH tag=DEV1 entry=password
# !KEEPASS group=meps/data_cloud title=SSH tag=DEV1 entry=host
def test_find_entry(kp):
    group = kp.find_groups(name="meps/data_cloud", first=True)
    ssh_dev1_entry, *_ = kp.find_entries(group=group, title="SSH", tags=["DEV1"])
    assert ssh_dev1_entry.title == "SSH"
    assert ssh_dev1_entry.username == "syrocon"
    assert ssh_dev1_entry.password == "syroconsyrocon"
    # access custom properties
    assert ssh_dev1_entry.custom_properties["host"] == "1.2.3.4"


def test_parse_line_to_dict():
    line = "  group  =meps/data_cloud title = SSH tag=DEV1 entry =username\n"
    rx_dict = {
        "group": re.compile(r"group[\s]*=[\s]*([\w/]*)"),
        "title": re.compile(r"title[\s]*=[\s]*([\w]*)"),
        "tag": re.compile(r"tag[\s]*=[\s]*([\w]*)"),
        "entry": re.compile(r"entry[\s]*=[\s]*([\w]*)"),
    }
    result = {}
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            result[key] = match.group(1)
    assert result == {
        "group": "meps/data_cloud",
        "title": "SSH",
        "tag": "DEV1",
        "entry": "username",
    }


# -- negative tests


def test_load_unknown_database_file():
    with pytest.raises(FileNotFoundError):
        _ = PyKeePass("unknown.kbdx", password="syrocon")


def test_wrong_master_password(path):
    with pytest.raises(CredentialsIntegrityError):
        _ = PyKeePass(path, password="wrong")
