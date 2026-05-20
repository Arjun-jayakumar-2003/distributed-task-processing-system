from django.urls import path
from .views import create_task , get_task

urlpatterns = [
    path("tasks/", create_task, name="create_task"),
    path("tasks/<int:task_id>/", get_task),
]