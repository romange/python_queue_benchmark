import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats_async

from tasks import broker, load_test_job

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))


async def enqueue_jobs():
    await broker.startup()
    start_time = time.time()
    for i in range(total_jobs):
        await load_test_job.kiq(i)
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")
    await print_memory_stats_async()
    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(enqueue_jobs())
