import concurrent
import logging
import threading
import time

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def thread_function(name):  # local variables are thread-safe
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


def test_thread_1():
    logging.info("Main    : before creating thread")
    t = threading.Thread(target=thread_function, args=(1,), daemon=True)
    logging.info("Main    : before running thread")
    t.start()
    logging.info("Main    : wait for the thread to finish")
    t.join()
    logging.info("Main    : all done")


def test_thread_2():
    threads = []
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        t = threading.Thread(target=thread_function, args=(index,))
        threads.append(t)
        t.start()
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)


def test_thread_3():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # for index in range(3):
        #     executor.submit(thread_function, index)  # 'submit' allows positional and keyword arguments
        executor.map(thread_function, range(3))
        # context manager makes '.join()'


def test_thread_4():
    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.locked_update, index)
    logging.info("Testing update. Ending value is %d.", database.value)


class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        # context manager calls '.acquire()' and '.release()'
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)
