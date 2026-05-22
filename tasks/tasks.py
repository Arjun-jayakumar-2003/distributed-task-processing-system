from celery import shared_task
from time import sleep

from .models import Task


@shared_task
def process_task(task_id):

    task = Task.objects.get(id=task_id)

    task.status = "PROCESSING"
    task.save()

    sleep(5)

    task.result = f"Processed payload: {task.payload}"

    task.status = "SUCCESS"
    task.save()