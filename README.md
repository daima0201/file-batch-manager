# file-batch-manager



- 前端部署

  - ```bash
    # 安装依赖
    npm install
    
    # 开发模式
    npm run serve
    
    # 生产构建
    npm run build
    
    # 部署构建后的文件到Nginx
    ```

    

- 后端部署

  - ```bash
    # 创建虚拟环境
    
    python -m venv venv
    source venv/bin/activate
    
    # 安装依赖
    
    pip install django djangorestframework mysqlclient django-cors-headers
    
    # 数据库迁移
    
    python manage.py makemigrations
    python manage.py migrate
    
    # 创建超级用户
    
    python manage.py createsuperuser
    
    # 运行开发服务器
    
    python manage.py runserver 0.0.0.0:8000
    
    # 生产环境建议使用Gunicorn
    
    pip install gunicorn
    gunicorn file_manager.wsgi:application -b 0.0.0.0:8000
    ```

