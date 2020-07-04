import os

from dotenv import load_dotenv


def test_dotenv():
    load_dotenv(verbose=True)
    assert os.getenv("GREET") == "Hallo Heike!"
