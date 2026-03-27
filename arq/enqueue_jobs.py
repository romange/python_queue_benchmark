import asyncio
import os
import sys
import time
from arq import create_pool
from arq.connections import RedisSettings
from tasks import load_test_job

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats_async

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))


async def enqueue_jobs():
    redis = await create_pool(RedisSettings())
    start_time = time.time()
    for i in range(total_jobs):
        queue_name = f"queue_{i % num_queues}"
        await redis.enqueue_job("load_test_job", i, _queue_name=queue_name)
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")
    await print_memory_stats_async(redis)


if __name__ == "__main__":
    asyncio.run(enqueue_jobs())
