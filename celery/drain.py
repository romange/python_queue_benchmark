import os
import time

from celery_config import app
from redis import Redis

num_queues = int(os.getenv("NUM_QUEUES", 10))
poll_interval = int(os.getenv("POLL_INTERVAL", 2))

r = Redis()
queue_keys = [f"queue_{i}" for i in range(num_queues)]


def drain_and_shutdown():
    while True:
        total = sum(r.llen(k) for k in queue_keys)

        i = app.control.inspect()
        active = i.active() or {}
        reserved = i.reserved() or {}
        total_processing = sum(len(tasks) for tasks in active.values()) + sum(
            len(tasks) for tasks in reserved.values()
        )

        if total == 0 and total_processing == 0:
            print("All queues empty and all workers idle. Shutting down...")
            app.control.shutdown()
            break

        time.sleep(poll_interval)


if __name__ == "__main__":
    drain_and_shutdown()
