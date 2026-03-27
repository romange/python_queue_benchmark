import os
import sys
import time
from redis import Redis
from rq import Queue
from tasks import load_test_job

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats

redis_conn = Redis()

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))

queues = [Queue(f"queue_{i}", connection=redis_conn) for i in range(num_queues)]


def enqueue_jobs():
    start_time = time.time()
    for i in range(total_jobs):
        queues[i % num_queues].enqueue(load_test_job, i)
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")
    print_memory_stats(redis_conn)


if __name__ == "__main__":
    enqueue_jobs()
