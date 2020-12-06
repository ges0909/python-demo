import signal
import time

from contextlib import contextmanager
from time import time, sleep


class Timer:
    def __init__(self):
        self._start = None
        self.elapsed = 0.0

    def start(self):
        if self._start is not None:
            raise RuntimeError("Timer already started...")
        self._start = time.perf_counter()

    def stop(self):
        if self._start is None:
            raise RuntimeError("Timer not yet started...")
        end = time.perf_counter()
        self.elapsed += end - self._start
        self._start = None

    def __enter__(self):  # setup
        self.start()
        return self  # return value used in "with ... as <var>:"

    def __exit__(self, *args):  # teardown
        self.stop()


def test_timer():
    manager = Timer()
    manager.__enter__()
    time.sleep(3)  # body
    manager.__exit__(None, None, None)
    print(manager.elapsed)


def test_timer_2():
    with Timer() as manager:
        time.sleep(3)
    print(manager.elapsed)


# --


@contextmanager
def timed(label):
    start = time()  # Setup - __enter__
    print(f"{label}: Start at {start}")
    try:
        yield  # yield to body of `with` statement
    finally:  # Teardown - __exit__
        end = time()
        print(f"{label}: End at {end} ({end - start} elapsed)")


def test_timer_3():
    with timed("Counter"):
        sleep(3)


# --


class timeout:
    def __init__(self, seconds, *, timeout_message=""):
        self.seconds = int(seconds)
        self.timeout_message = timeout_message

    def _timeout_handler(self, signum, frame):
        raise TimeoutError(self.timeout_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self._timeout_handler)  # Set handler for SIGALRM
        signal.alarm(self.seconds)  # start countdown for SIGALRM to be raised

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)  # Cancel SIGALRM if it's scheduled
        return exc_type is TimeoutError  # Suppress TimeoutError


def test_timeout():
    with timeout(3):
        # Some long running task...
        sleep(10)
