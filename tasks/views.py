from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

from django.shortcuts import get_object_or_404

@api_view(["POST"])
def create_task(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    serializer = TaskSerializer(task)

    return Response(serializer.data)