"""
ASGI config for ninja_xia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from backend.xia.common.redis import RedisCli
from backend.xia.common.task import scheduler

# 初始化redis连接
RedisCli.init_redis_connect()

# 定时任务随系统启动
scheduler.start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ninja_xia.settings')

application = get_asgi_application()
