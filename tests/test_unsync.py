import asyncio
import time
from random import randint, randrange

from unsync import unsync


@unsync
async def async_about(delay) -> int:
    await asyncio.sleep(delay)
    return delay


@unsync
def sync_about(delay) -> int:
    time.sleep(delay)
    return delay


# '@unsync' uses coroutines
def test_unsync_async_func():
    futures = []
    for _ in range(0, 100):
        delay = randint(0, 3)
        futures.append(async_about(delay=delay))

    for f in futures:
        print(f.result())


# '@unsync' uses threads
def test_unsync_sync_func():
    futures = []
    for _ in range(0, 100):
        delay = randrange(3)
        futures.append(sync_about(delay=delay))

    for f in futures:
        print(f.result())


# -- async ssh


async def ssh_client(greet: str) -> str:
    # async with asyncssh.connect(host="172.17.113.209", username="test", password="test", known_hosts=None,) as conn:
    #     result = await conn.run(f"echo {greet}")
    #     return result.stdout
    await asyncio.sleep(1)
    return greet


async def main():
    tasks = [ssh_client("Dobar dan"), ssh_client("Buon giorno"), ssh_client("Guten Tag")]
    results = await asyncio.gather(*tasks)
    for r in results:
        print(r)


async def main2():
    tasks = [ssh_client("Dobar dan"), ssh_client("Buon giorno"), ssh_client("Guten Tag")]
    for future in asyncio.as_completed(tasks):
        result = await future
        print(result)


def test_ssh():
    asyncio.run(main())


def test_future():
    asyncio.run(main2())
