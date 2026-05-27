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

    logger.info(
        "task_processing_started",
        extra={
            "task_id": task_id,
            "status": "",
            "retry_count": "",
            "error": "",
        }
    )

    task = Task.objects.get(id=task_id)

    logger.info(
        "task_fetched_successfully",
        extra={
            "task_id": task_id,
            "status": "",
            "retry_count": "",
            "error": "",
        }
    )

    task.status = "PROCESSING"
    task.processing_started_at = timezone.now()
    task.save()

    logger.info(
        "task_moved_to_processing",
        extra={
            "task_id": task_id,
            "status": task.status,
            "retry_count": "",
            "error": "",
        }
    )

    try:
        
        sleep(5)

        task.result = f"Processed payload: {task.payload}"
        

        task.status = "SUCCESS"
        task.processing_completed_at = timezone.now()
        task.error_message = None
        task.save()

        logger.info(
            "task_completed_successfully",
            extra={
                "task_id": task_id,
                "status": task.status,
                "retry_count": task.retry_count,
                 "error": "",
            }
        )

    except Exception as e:
        task.status = "FAILED"
        task.processing_completed_at = timezone.now()
        task.error_message = str(e)
        task.retry_count = self.request.retries
        task.save()

        logger.error(
            "task_failed",
            extra={
                "task_id": task_id,
                "status": task.status,
                "retry_count": task.retry_count,
                "error": str(e),
            }
        )

        logger.warning(
            "task_retrying",
            extra={
                "task_id": task_id,
                "status": task.status,
                "retry_count": self.request.retries,
                "error": str(e),
            }
        )

        raise