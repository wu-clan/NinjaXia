"""
WSGI config for ninja_xia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from backend.common.redis import RedisCli
from backend.common.task import scheduler

# 初始化redis连接
RedisCli.init_redis_connect()

# 定时任务随系统启动
scheduler.start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ninja_xia.settings')

application = get_wsgi_application()
