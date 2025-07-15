from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task-list'),  # 实际路径：/filemanager/scanner/tasks
]
