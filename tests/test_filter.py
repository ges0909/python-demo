import operator

import pytest


class InvalidQuery(Exception):
    pass


class Filter(object):
    binary_operators = {
        "=": operator.eq,
        "==": operator.eq,
        "eq": operator.eq,
        "<": operator.lt,
        "lt": operator.lt,
        ">": operator.gt,
        "gt": operator.gt,
        "<=": operator.le,
        "≤": operator.le,
        "le": operator.le,
        ">=": operator.ge,
        "≥": operator.ge,
        "ge": operator.ge,
        "!=": operator.ne,
        "≠": operator.ne,
        "ne": operator.ne,
    }

    multiple_operators = {
        "or": any,
        "∨": any,
        "and": all,
        "∧": all,
    }

    def __init__(self, tree):
        self._eval = self.build_evaluator(tree)

    def __call__(self, **kwargs):
        return self._eval(kwargs)

    def build_evaluator(self, tree):
        try:
            _operator, nodes = list(tree.items())[0]
        except Exception:
            raise InvalidQuery("Unable to parse tree %s" % tree)
        try:
            op = self.multiple_operators[_operator]
        except KeyError:
            try:
                op = self.binary_operators[_operator]
            except KeyError:
                raise InvalidQuery("Unknown operator %s" % _operator)
            assert len(nodes) == 2  # binary operators take 2 values

            def _op(values):
                return op(values[nodes[0]], nodes[1])

            return _op
        # Iterate over every item in the list of the value linked
        # to the logical operator, and compile it down to its own
        # evaluator.
        elements = [self.build_evaluator(node) for node in nodes]
        return lambda values: op((e(values) for e in elements))


@pytest.fixture
def filter_example():
    return Filter({"and": [{"eq": ("foo", 3)}, {"gt": ("bar", 4)},]},)


def test_filter_1(filter_example):
    assert filter_example(foo=3, bar=5)


def test_filter_2(filter_example):
    assert not filter_example(foo=4, bar=5)
