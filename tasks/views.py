from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

from django.shortcuts import get_object_or_404

from .tasks import process_task

@api_view(["GET", "POST"])
def tasks(request):

    if request.method == "GET":

        status_filter = request.query_params.get("status")

        tasks = Task.objects.all()

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()
            process_task.delay(task.id)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["GET"])
def get_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    serializer = TaskSerializer(task)

    return Response(serializer.data)

