from taskiq_redis import RedisStreamBroker

broker = RedisStreamBroker(url="redis://localhost:6379", queue_name="taskiq_bench")


@broker.task
async def load_test_job(num):
    return
