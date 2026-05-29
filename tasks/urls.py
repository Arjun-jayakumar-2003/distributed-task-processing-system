from django.urls import path
from .views import tasks , get_task , health_check

urlpatterns = [
    path("tasks/", tasks, name="tasks"),
    path("tasks/<int:task_id>/", get_task),
    path("health/", health_check),
]