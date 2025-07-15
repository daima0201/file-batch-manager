"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# 设置 Django 的配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 获取 WSGI 应用对象
application = get_wsgi_application()