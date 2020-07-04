from inspect import getmembers


def any_func():
    pass


def test_inspect_function_name():
    results = getmembers(any_func)
    for name, data in results:
        print(f"{name}")
