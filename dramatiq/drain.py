import os
import signal
import sys
import time

from redis import Redis

num_queues = int(os.getenv("NUM_QUEUES", 10))
poll_interval = int(os.getenv("POLL_INTERVAL", 2))
worker_pid = int(sys.argv[1])

r = Redis()
queue_keys = [f"{{dr}}:queue_{i}" for i in range(num_queues)]


def drain_and_shutdown():
    while True:
        total = sum(r.llen(k) for k in queue_keys)
        if total == 0:
            print("All queues empty. Shutting down...")
            os.kill(worker_pid, signal.SIGTERM)
            break
        time.sleep(poll_interval)


if __name__ == "__main__":
    drain_and_shutdown()
