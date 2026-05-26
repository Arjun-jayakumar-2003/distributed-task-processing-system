from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("PROCESSING", "PROCESSING"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    
    payload = models.JSONField()
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def processing_duration(self):
        if self.processing_started_at and self.processing_completed_at:
            return (
                self.processing_completed_at
                - self.processing_started_at
            )

        return None