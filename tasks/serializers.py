from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    processing_duration = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = "__all__"