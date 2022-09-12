#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import signal
import sys

from django.dispatch import Signal


def shutdown_event(*args):
    # server
    Signal().send('system')
    # runserver
    if os.environ.get('RUN_MAIN') == 'true':
        # 关闭redis连接
        from backend.xia.common.redis import redis_client
        redis_client.close()

        # 关闭定时任务
        from backend.xia.common.task import scheduler
        scheduler.shutdown()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown_event)
