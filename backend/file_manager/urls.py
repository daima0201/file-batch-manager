from django.urls import path, include
from backend.file_manager import views

urlpatterns = [
    path('', views.homepage, name='home'),  # 实际路径：/filemanager/

    # 子应用专属路由
    # path('dashboard/', views.dashboard, name='dashboard'),  # 实际路径：/filemanager/dashboard/
    path('operation/', include('backend.operations.urls')),  # 实际路径：/filemanager/operation/
    path('scanner/', include('backend.scanner.urls')),  # 实际路径：/filemanager/scanner/

]
