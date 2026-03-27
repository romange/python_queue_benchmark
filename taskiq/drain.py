import os
import signal
import sys
import time

from redis import Redis

poll_interval = int(os.getenv("POLL_INTERVAL", 2))
worker_pid = int(sys.argv[1])

r = Redis()


def drain_and_shutdown():
    while True:
        groups = r.xinfo_groups("taskiq_bench")
        if groups:
            group = groups[0]
            lag = group.get("lag", 0) or 0
            pending = group.get("pending", 0) or 0
            if lag == 0 and pending == 0:
                print("All messages consumed. Shutting down...")
                os.kill(worker_pid, signal.SIGTERM)
                break
        time.sleep(poll_interval)


if __name__ == "__main__":
    drain_and_shutdown()
