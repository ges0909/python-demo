import logging

import pytest
from pydantic import validate_arguments, ValidationError

logger = logging.getLogger(__name__)


@validate_arguments
def repeat(s: str, count: int, *, separator: bytes = b"") -> bytes:
    b = s.encode()
    return separator.join(b for _ in range(count))


def test_positional_args():
    assert repeat("hello", 3) == b"hellohellohello"


def test_positional_and_keyword_args():
    assert repeat("x", "4", separator=b" ") == b"x x x x"


def test_validation_error():
    with pytest.raises(ValidationError):
        repeat("hello", "wrong")


def test_catch_validation_error():
    try:
        _ = repeat("hello", "wrong")
    except ValidationError as error:
        print("\n" + str(error))
        logger.error("%s", str(error))
