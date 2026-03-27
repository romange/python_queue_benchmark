import logging
import os
import time
from tasks import load_test_job


<<<<<<< Updated upstream
total_jobs = os.getenv("TOTAL_JOBS", 20000)
=======
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Enable kombu/celery connection logging
logging.getLogger("kombu").setLevel(logging.DEBUG)
logging.getLogger("celery").setLevel(logging.DEBUG)

total_jobs = int(os.getenv("TOTAL_JOBS", 200000))
num_queues = int(os.getenv("NUM_QUEUES", 10))
LOG_INTERVAL = 10000
>>>>>>> Stashed changes


def enqueue_jobs():
    start_time = time.time()
    for i in range(total_jobs):
<<<<<<< Updated upstream
        print(f"Enqueuing job {i}")
        load_test_job.delay(i)
=======
        try:
            load_test_job.apply_async(args=[i], queue=f"queue_{i % num_queues}", ignore_result=True)
        except Exception as e:
            logger.error(f"Failed to enqueue job {i}: {e}")
            raise
        if (i + 1) % LOG_INTERVAL == 0:
            elapsed = time.time() - start_time
            logger.info(f"Enqueued {i + 1}/{total_jobs} in {elapsed:.1f}s ({(i+1)/elapsed:.0f} jobs/sec)")
>>>>>>> Stashed changes
    end_time = time.time()
    print("All jobs enqueued within: ", end_time - start_time, "seconds")


if __name__ == "__main__":
    enqueue_jobs()
