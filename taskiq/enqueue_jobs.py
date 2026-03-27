import asyncio
import os
import sys
import time
from taskiq_redis import RedisStreamBroker

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats_async

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))

REDIS_URL = "redis://localhost:6379"


def _make_broker_task(queue_name):
    broker = RedisStreamBroker(url=REDIS_URL, queue_name=queue_name)

    @broker.task
    async def load_test_job(num):
        end_time = time.time()
        print(f"Job {num} finished at {end_time}")

    return broker, load_test_job


broker_tasks = [_make_broker_task(f"queue_{i}") for i in range(num_queues)]
brokers = [bt[0] for bt in broker_tasks]
task_fns = [bt[1] for bt in broker_tasks]


async def enqueue_jobs():
    for broker in brokers:
        await broker.startup()
    start_time = time.time()
    for i in range(total_jobs):
        await task_fns[i % num_queues].kiq(i)
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")
    await print_memory_stats_async()
    for broker in brokers:
        await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(enqueue_jobs())
