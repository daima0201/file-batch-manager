from django.urls import path, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r'files', views.FileTreeViewSet, basename='filetree')
router.register(r'operations', views.OperationLogViewSet, basename='operationlog')
router.register(r'scan', views.ScanViewSet, basename='scan')
router.register(r'file-ops', views.FileOperationViewSet, basename='file-ops')

urlpatterns = [
    path('', include(router.urls)),
]
