import os

from celery import Celery

from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL",
    "redis://localhost:6379/0"
)

app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND",
    "redis://localhost:6379/0"
)

app.conf.accept_content = ["json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"

app.conf.timezone = "UTC"

app.conf.task_queues = (
    Queue("default"),
    Queue("high_priority"),
    Queue("low_priority"),
)

app.conf.task_default_queue = "default"

app.autodiscover_tasks()