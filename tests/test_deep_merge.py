from deepmerge import always_merger


def test_deep_merge():
    d1 = {
        "a": 1,
        "b": 2,
        "l": [1, 2],
        "d": {"x": "x"},
    }
    d2 = {
        "b": 1,
        "c": 3,
        "l": [3],
        "d": {"y": "y", "z": "z"},
    }
    d = always_merger.merge(d1, d2)
    assert d == {
        "a": 1,
        "b": 1,
        "c": 3,
        "l": [1, 2, 3],
        "d": {"x": "x", "y": "y", "z": "z"},
    }
