# -*-coding:utf-8-*-

"""
@author: teddy
@file: test_asyncio.py
@time: 2020/4/12 10:42 AM
@description:
"""
import asyncio
from threading import Thread

Thread.isDaemon()


async def async_func(i):
    print(f"[start]:{i}")
    await asyncio.sleep(1)
    import time

    # time.sleep(1)
    print(f"[end]:{i}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [async_func(i) for i in range(100)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
