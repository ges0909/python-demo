from collections import OrderedDict


def _flatten(dict_, keys=()):
    flatten_dict = OrderedDict()  # keep original order
    if isinstance(dict_, dict):
        for key, value in dict_.items():
            _flatten_dict = _flatten(value, keys=keys + (str(key),))
            flatten_dict = {**flatten_dict, **_flatten_dict}
    elif isinstance(dict_, list):
        for index, value in enumerate(dict_):
            _flatten_dict = _flatten(value, keys=keys + (str(index),))
            flatten_dict = {**flatten_dict, **_flatten_dict}
    else:
        flatten_dict[keys] = dict_
    return flatten_dict


def flatten(value):
    flatten_dict = _flatten(value)
    return {".".join(key): value_ for key, value_ in flatten_dict.items()}


# -- tests


def test_dict():
    d = {
        "a": {"b": "c"},
        1: 2,
        "x": {"y": "yy", "z": {"zz": "xyz"}, },
    }
    d_ = _flatten(d)
    assert d_ == {
        ("a", "b"): "c",
        ("1",): 2,
        ("x", "y"): "yy",
        ("x", "z", "zz"): "xyz",
    }


def test_list():
    d = {"a": [1, 2, 3]}
    d_ = _flatten(d)
    assert d_ == {
        ("a", "0"): 1,
        ("a", "1"): 2,
        ("a", "2"): 3,
    }


def test_dict_table():
    d = {
        "a": {"b": "c"},
        1: 2,
        "x": {"y": "yy", "z": {"zz": "xyz"}, },
    }
    t = flatten(d)
    assert t == {
        "a.b": "c",
        "1": 2,
        "x.y": "yy",
        "x.z.zz": "xyz",
    }


def test_list_table():
    d = {"a": [1, 2, 3]}
    t = flatten(d)
    assert t == {
        "a.0": 1,
        "a.1": 2,
        "a.2": 3,
    }


def test_table():
    d = {
        "a": {"b": "c"},
        1: 2,
        "x": {"y": "yy", "z": {"zz": "xyz"}, },
        "l": [1, 2, 3],
    }
    t = flatten(d)
    assert t == {
        "a.b": "c",
        "1": 2,
        "x.y": "yy",
        "x.z.zz": "xyz",
        "l.0": 1,
        "l.1": 2,
        "l.2": 3,
    }
