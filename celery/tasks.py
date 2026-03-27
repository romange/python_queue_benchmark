from celery_config import app


@app.task
def load_test_job(num):
    return
