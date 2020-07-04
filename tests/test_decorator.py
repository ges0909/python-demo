import functools
import logging
from itertools import groupby
from pprint import PrettyPrinter

from box import Box, BoxKeyError

logging.basicConfig(filename="decorator.log", level=logging.DEBUG)

logger = logging.getLogger(__name__)


def log(func):
    pp = PrettyPrinter(indent=4)

    @functools.wraps(func)  # for proper access to 'func.__name__'
    def wrapper(*args, **kwargs):
        _args = [pp.pformat(arg) for arg in args]
        _args.extend([f"{str(k)}={pp.pformat(v)}" for k, v in kwargs.items()])
        logger.debug("action '%s': << %s", func.__name__, ", ".join(_args))
        result = func(*args, **kwargs)
        logger.debug("action '%s': >> %s", func.__name__, pp.pformat(result))
        return result

    return wrapper


def box(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _args = Box(*args, box_dots=True, conversion_box=False)
        _kwargs = Box(**kwargs, box_dots=True, conversion_box=False)
        return func(*args, **_kwargs)

    return wrapper


def check(*params):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args, kwargs):
            for key, type_ in params:
                try:
                    value = kwargs[key]
                except BoxKeyError:
                    # logger.error("action '%s': parameter '%s' is missing", func.__name__, key)
                    raise KeyError(f"action '{func.__name__}': parameter '{key}' is missing")
                if not value:
                    # logger.error("action '%s': parameter '%s' is null", func.__name__, key)
                    raise ValueError(f"action '{func.__name__}': parameter '{key}' is null")
                if not isinstance(value, type_):
                    # logger.error(
                    #     "action '%s': parameter '%s' has wrong type '%s', expected '%s'",
                    #     func.__name__,
                    #     key,
                    #     type(value).__name__,
                    #     type_.__name__,
                    # )
                    raise TypeError(
                        f"action '{func.__name__}': parameter '{key}' has wrong type '{type(value).__name__}', expected '{type_.__name__}'"
                    )
            return func(args, kwargs)

        return wrapper

    return decorator


def loop(*params):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for var in params:
                for value in kwargs[var]:
                    kwargs[var] = value
                    result = func(*args, **kwargs)
                    results.append(result)
            return results

        return wrapper

    return decorator


@log
@box
# @check(("args.ids", list))
@loop("args.ids")
def simple(args, env, props, item):
    return {"status": args.ids}


def test_iterate():
    result = simple(args={"ids": [1, 2, 3]}, env={}, props={}, item={})
    # assert result == [{"status": 1}, {"status": 2}, {"status": 3}]


def test_groupby():
    l = [{"status": 1, "letter": "a"}, {"status": 2, "letter": "b"}, {"status": 3, "letter": "c"}]
    results = []
    for key, group in groupby(l, lambda d: list(d.keys())[0]):
        for g in group:
            pass
        results.append({key: [list(g.values())[0] for g in group]})
    assert results == [{"status": [1, 2, 3]}, {"letter": ["a", "b", "c"]}]
