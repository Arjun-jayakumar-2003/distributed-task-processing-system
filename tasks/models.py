from django.db import models


class Task(models.Model):
    status = models.CharField(max_length=20)
    payload = models.JSONField()
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)