import asyncio
import os
import sys
import time

from tasks import app, load_test_job

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))


async def enqueue_jobs():
    async with app.open_async():
        start_time = time.time()
        for i in range(total_jobs):
            await load_test_job.defer_async(num=i, queue=f"queue_{i % num_queues}")
        end_time = time.time()
        print("All jobs enqueued within: ", end_time - start_time, "seconds")

    from redis import Redis
    redis_conn = Redis()
    print_memory_stats(redis_conn)


if __name__ == "__main__":
    asyncio.run(enqueue_jobs())
