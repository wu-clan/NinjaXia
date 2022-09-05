#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ninja_xia.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # 初始化redis连接
    from backend.xia.common.redis import RedisCli
    RedisCli.init_redis_connect()

    # 定时任务随系统启动
    from backend.xia.common.task import scheduler
    scheduler.start()


if __name__ == '__main__':
    main()
