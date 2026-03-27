import os
import sys
import time
from tasks import load_test_job

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_stats import print_memory_stats

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))


def enqueue_jobs():
    from redis import Redis
    redis_conn = Redis()
    start_time = time.time()
    for i in range(total_jobs):
        load_test_job.send_with_options(args=(i,), queue_name=f"queue_{i % num_queues}")
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")
    print_memory_stats(redis_conn)


if __name__ == "__main__":
    enqueue_jobs()
