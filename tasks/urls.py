from django.urls import path
from .views import tasks , get_task

urlpatterns = [
    path("tasks/", tasks, name="tasks"),
    path("tasks/<int:task_id>/", get_task),
]