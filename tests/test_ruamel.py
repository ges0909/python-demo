import collections
import re

from ruamel.yaml import YAML

doc = """
example: something
endpoint: http://www.google.com  #     report  
list:
    - 1
    - 2 # 3
    - 3
list2:  # 2
    - a
    - b
    - c
password: !ENVIRON SECRET_VAR
password2: !KEEPASS group=meps/data_cloud title=SSH tag=DEV1 entry=password
"""


class Environ:
    yaml_tag = "!ENVIRON"

    @classmethod
    def from_yaml(cls, constructor, node):
        if node.value == "SECRET_VAR":
            return "my little secret"
        return None


class KeePass:
    yaml_tag = "!KEEPASS"

    @classmethod
    def from_yaml(cls, constructor, node):
        rx_dict = {
            "group": re.compile(r"group[\s]*=[\s]*([\w/]*)"),
            "title": re.compile(r"title[\s]*=[\s]*([\w]*)"),
            "tag": re.compile(r"tag[\s]*=[\s]*([\w]*)"),
            "entry": re.compile(r"entry[\s]*=[\s]*([\w]*)"),
        }
        result = {}
        for key, rx in rx_dict.items():
            match = rx.search(node.value)
            if match:
                result[key] = match.group(1)
        # access here to keepass database file
        return "not implemented"


def test_custom_tag():
    yaml = YAML()
    yaml.register_class(Environ)
    yaml.register_class(KeePass)
    data = yaml.load(doc)
    assert data["password"] == "my little secret"


def test_comment():
    yaml = YAML(typ="rt")  # typ="safe", pure=True
    data = yaml.load(doc)
    for key, comment in data.ca.items.items():
        if re.match("^#[\s]*report[\s]*$", comment[2].value):
            assert key in ("endpoint", "list2")
    # comment on list element
    assert data["list"].ca.items[1][0].value == "# 3\n"


def test_line_number():
    yaml = YAML()  # default: typ="rt" (round-trip)
    data = yaml.load(doc)
    assert isinstance(data["list"], collections.Iterable)  # property 'lc' can be accessed on collection items only
    assert data["list"].lc.line == 4
    assert data["list2"].lc.line == 8
