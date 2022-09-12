"""
WSGI config for ninja_xia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.ninja_xia.settings')

application = get_wsgi_application()

# 初始化redis连接
from backend.xia.common.redis import RedisCli  # noqa

RedisCli().init_redis_connect()

# 定时任务随系统启动
from backend.xia.common.task import scheduler  # noqa

scheduler.start()
