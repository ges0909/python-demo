import functools
from functools import partial


def multiply(x, y):
    return x * y


def test_double():
    func = partial(multiply, 2)
    assert func(3) == 6


def test_triple():
    func = partial(multiply, 3)
    assert func(3) == 9


def order_func(a, b, c, d):
    return a * 4 + b * 3 + c * 2 + d


def test_order_func():
    func = partial(order_func, c=5, d=6)
    assert func(8, 4) == 60


def test_metadata():
    func = partial(multiply, x=2)
    print(func.func)
    print(func.keywords)


def test_metadata_wrapper():
    func = partial(multiply, x=2)
    # print(func.__name__)  # AttributeError: 'functools.partial' object has no attribute '__name__'
    functools.update_wrapper(func, multiply)
    print(func.__name__)
