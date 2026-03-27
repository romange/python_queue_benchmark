import os
import sys
import time
from huey import RedisHuey

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))


def _make_queue_task(queue_name):
    h = RedisHuey(name=queue_name)

    @h.task()
    def load_test_job(num):
        end_time = time.time()
        print(f"Job {num} finished at {end_time}")

    return load_test_job


task_fns = [_make_queue_task(f"queue_{i}") for i in range(num_queues)]


def enqueue_jobs():
    from redis import Redis
    redis_conn = Redis()
    start_time = time.time()
    for i in range(total_jobs):
        task_fns[i % num_queues](i)
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")
    print_memory_stats(redis_conn)


if __name__ == "__main__":
    enqueue_jobs()
