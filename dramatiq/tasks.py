import os

import dramatiq
from dramatiq.brokers.redis import RedisBroker

num_queues = int(os.getenv("NUM_QUEUES", 10))

broker = RedisBroker(url="redis://localhost:6379", namespace="{dr}")
dramatiq.set_broker(broker)

for i in range(num_queues):
    broker.declare_queue(f"queue_{i}")


@dramatiq.actor
def load_test_job(num):
    return
