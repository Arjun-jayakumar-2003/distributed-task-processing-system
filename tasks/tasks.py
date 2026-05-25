from celery import shared_task
from time import sleep

from django.utils import timezone

from .models import Task

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def process_task(self, task_id):

    task = Task.objects.get(id=task_id)

    task.status = "PROCESSING"
    task.processing_started_at = timezone.now()
    task.save()

    try:
        
        sleep(5)

        task.result = f"Processed payload: {task.payload}"
        

        task.status = "SUCCESS"
        task.processing_completed_at = timezone.now()
        task.error_message = None
        task.save()

    except Exception as e:
        task.status = "FAILED"
        task.processing_completed_at = timezone.now()
        task.error_message = str(e)
        task.retry_count = self.request.retries
        task.save()

        print(e)

        raise