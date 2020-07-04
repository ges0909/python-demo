import operator
import re
from contextlib import redirect_stdout
from enum import auto, Enum
from io import StringIO
from timeit import timeit


def test_how_to_add_a_new_key_to_a_dict():
    d: dict = {"x": 1, "y": 2}
    d["z"] = 3
    assert d == {"x": 1, "y": 2, "z": 3}


def test_how_to_merge_two_dicts():
    x = {"a": 1, "b": 2}
    y = {"b": 3, "c": 4}
    z = {**x, **y}
    assert z == {"a": 1, "b": 3, "c": 4}


def test_how_to_sort_a_dict_by_value():
    _xs = {"a": 4, "b": 3, "c": 2, "d": 1}
    # variant 1
    actual = sorted(_xs.items(), key=lambda x: x[1])
    assert actual == [("d", 1), ("c", 2), ("b", 3), ("a", 4)]
    # variant 2
    actual = sorted(_xs.items(), key=operator.itemgetter(1))
    assert actual == [("d", 1), ("c", 2), ("b", 3), ("a", 4)]


def test_how_to_pretty_print_a_dict():
    dict_ = {"a": 23, "b": 42, "c": 0xC0FFEE}
    import json

    print("\n" + json.dumps(dict_, indent=4, sort_keys=True))


def test_how_check_multiple_flags_at_once():
    _x, _y, _z = 0, 1, 0
    assert _x == 1 or _y == 1 or _z == 1
    assert _x or _y or _z
    assert 1 in (_x, _y, _z)
    assert any((_x, _y, _z))


def test_get_dict_method_with_default_value():
    dict_ = {
        382: "Alice",
        590: "Bob",
        951: "Dilbert",
    }

    def greeting(user_id):
        return "Hi %s!" % dict_.get(user_id, "there")

    assert greeting(382) == "Hi Alice!"
    assert greeting(333333) == "Hi there!"


def test_function_argument_unpacking():
    def func(x, y, z):
        print(x, y, z)

    out = StringIO()
    with redirect_stdout(out):
        tuple_ = (1, 0, 1)
        func(*tuple_)
        assert out.getvalue() == "1 0 1\n"

    out = StringIO()
    with redirect_stdout(out):
        dict_ = {"x": 1, "y": 0, "z": 1}
        func(**dict_)
        assert out.getvalue() == "1 0 1\n"


def test_timeit():
    timeit('"-".join(str(n) for n in range(100))', number=10000)
    timeit('"-".join([str(n) for n in range(100)])', number=10000)
    timeit('"-".join(map(str, range(100)))', number=10000)


def test_on_empty_list():
    list_ = []
    assert len(list_) == 0
    assert list_ == []
    assert not list_


def test_in_place_value_swapping():
    a, b = 23, 43
    a, b = b, a
    assert a == 43
    assert b == 23


def test_enum():
    class Keys(Enum):
        test = auto()
        command = auto()
        verify = auto()

        @classmethod
        def names(cls) -> set:
            return {name for name, member in cls.__members__.items()}

    assert Keys.test.name == "test"
    assert Keys.command.name == "command"
    assert Keys.verify.name == "verify"

    assert Keys.names() == {"verify", "command", "test"}


def test_how_to_destruct_a_dict():
    d: dict = {
        "item": "http_status_code",
        "equal": "200",
    }
    item, operation = d.keys()
    assert item == "item"
    assert operation == "equal"

    value1, value2 = d.values()
    assert value1 == "http_status_code"
    assert value2 == "200"


def test_remove_trailing_underscore_from_string():
    s = "abc_"
    s = s.rstrip("_")
    assert s == "abc"

    s2 = "abc"
    s2 = s2.rstrip("_")
    assert s2 == "abc"


def test_emulate_switch():
    def dispatch_dict(op, x, y):
        return {"add": lambda: x + y, "sub": lambda: x - y, "mul": lambda: x * y, "div": lambda: x / y,}.get(
            op, lambda: None
        )

    assert dispatch_dict("add", 2, 1)() == 3
    assert dispatch_dict("sub", 2, 1)() == 1
    assert dispatch_dict("mul", 2, 1)() == 2
    assert dispatch_dict("div", 2, 1)() == 2


def test_access_to_nested_dict():
    d = {"a": {"b": {"c": "ABC"}}}
    assert d.get("a").get("b").get("c") == "ABC"
    assert d.get("a").get("c") is None
    assert d.get("c", {}).get("b") is None


def test_regex():
    groups = re.search(r"(data|file)@([\w.]+)", "file@template.json")
    assert groups.group(1) == "file"
    assert groups.group(2) == "template.json"


def destruct(value: str):
    item1 = item2 = item3 = item4 = None
    value = re.sub(r"[\s+]", "", value)  # strip spaces
    items = value.split(",")
    if len(items) >= 1:
        parts = items[0].split("@")
        if len(parts) >= 1:
            item1 = parts[0]
        if len(parts) >= 2:
            item2 = parts[1]
    if len(items) >= 2:
        parts = items[1].split("@")
        if len(parts) >= 1:
            item3 = parts[0]
        if len(parts) >= 2:
            item4 = parts[1]
    return item1, item2, item3, item4


def test_split():
    item1, item2, item3, item4 = destruct("file@template.json, data@data.json")
    assert item1 == "file"
    assert item2 == "template.json"
    assert item3 == "data"
    assert item4 == "data.json"

    item1, item2, item3, item4 = destruct("file@template.json")
    assert item1 == "file"
    assert item2 == "template.json"
    assert item3 is None
    assert item4 is None

    item1, item2, item3, item4 = destruct("abc")
    assert item1 == "abc"
    assert item2 is None
    assert item3 is None
    assert item4 is None


def test_ternary_operator():
    assert (len("abc") if "abc" else 0) == len("abc")
    assert (len("") if "" else 0) == 0
    # short hand
    assert (len("abc") or 0) == len("abc")
    assert (len("") or 0) == 0


def test_brute_force():
    import itertools

    for p in itertools.permutations("ABCD"):
        print(p)


def test_when_to_use_repr_vs_str_():
    import datetime

    today = datetime.date(2017, 2, 2)
    # result of __str__ should be readable
    assert str(today) == "2017-02-02"
    # result of __repr__ should be unambiguous
    assert repr(today) == "datetime.date(2017, 2, 2)"
