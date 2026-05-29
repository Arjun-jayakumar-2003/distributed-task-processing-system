from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer

from django.shortcuts import get_object_or_404
from django.db.models import Q

from .tasks import process_task

from rest_framework.pagination import PageNumberPagination

@api_view(["GET", "POST"])
def tasks(request):

    if request.method == "GET":

        status_filter = request.query_params.get("status")
        ordering = request.query_params.get("ordering")
        search = request.query_params.get("search")

        tasks = Task.objects.all()

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        if ordering:
            tasks = tasks.order_by(ordering)

        if search:
            tasks = tasks.filter(
                Q(status__icontains=search) |
                Q(payload__icontains=search) |
                Q(result__icontains=search) |
                Q(error_message__icontains=search)
            )
            

        paginator = PageNumberPagination()

        paginated_tasks = paginator.paginate_queryset(tasks, request)

        serializer = TaskSerializer(paginated_tasks, many=True)

        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()
            queue_name = (
                "high_priority"
                if task.priority == "HIGH"
                else "default"
            )

            process_task.apply_async(
                args=[task.id],
                queue=queue_name
            )

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

