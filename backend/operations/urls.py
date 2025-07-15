from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.operation_history, name='operation-history'),  # 实际路径：/filemanager/operation/history/
]
