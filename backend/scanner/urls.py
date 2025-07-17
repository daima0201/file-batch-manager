from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.trigger_scan),  # 实际路径：/filemanager/scanner/scan
    path('results/', views.scan_result),  # 实际路径：/filemanager/scanner/results
    path('status/', views.scan_status_view),  # 实际路径：/filemanager/scanner/status
]
