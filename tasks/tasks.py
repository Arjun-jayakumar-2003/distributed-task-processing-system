import logging

from celery import shared_task
from time import sleep

from django.utils import timezone

from .models import Task

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)
def process_task(self, task_id):

    logger.info(f"Starting task processing task_id={task_id}")

    task = Task.objects.get(id=task_id)

    logger.info(f"Task fetched successfully task_id={task_id}")

    task.status = "PROCESSING"
    task.processing_started_at = timezone.now()
    task.save()

    logger.info(f"Task moved to PROCESSING state task_id={task_id}")

    try:
        
        sleep(5)

        task.result = f"Processed payload: {task.payload}"
        

        task.status = "SUCCESS"
        task.processing_completed_at = timezone.now()
        task.error_message = None
        task.save()

        logger.info(f"Task completed successfully task_id={task_id}")

    except Exception as e:
        task.status = "FAILED"
        task.processing_completed_at = timezone.now()
        task.error_message = str(e)
        task.retry_count = self.request.retries
        task.save()

        logger.error(f"Task failed task_id={task_id} error={str(e)}")

        logger.warning(
            f"Retrying task task_id={task_id} retry_count={self.request.retries}"
        )

        raise