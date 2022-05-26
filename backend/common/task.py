#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from backend.ninja_xia import settings


def task_redis_conf():
    """
    task store

    :return:
    """
    redis_conf = {
        'host': settings.TASK_REDIS_HOST,
        'port': settings.TASK_REDIS_PORT,
        'password': settings.TASK_REDIS_PASSWORD,
        'db': settings.TASK_REDIS_DATABASE,
        'socket_timeout': settings.TASK_REDIS_TIMEOUT
    }

    return redis_conf


def task_executor_conf():
    """
    task executor conf

    :return:
    """
    executor = None

    pp_executor = ProcessPoolExecutor(settings.TASK_PP_EXECUTOR_MAX_WORKERS)
    tp_executor = ThreadPoolExecutor(settings.TASK_TP_EXECUTOR_MAX_WORKERS)

    if settings.TASK_TP_STATUS and settings.TASK_PP_STATUS:
        executor = {
            'default': pp_executor,
            'threadpool': tp_executor
        }

    if settings.TASK_PP_STATUS and not settings.TASK_TP_STATUS:
        executor = {
            'default': pp_executor
        }

    if settings.TASK_TP_STATUS and not settings.TASK_PP_STATUS:
        executor = {
            'default': tp_executor
        }

    return executor


def task_conf():
    """
    task conf

    :return:
    """
    end_conf = {
        # 配置存储器
        "jobstores": {
            'default': RedisJobStore(**task_redis_conf())
        },
        # 配置执行器
        "executors": task_executor_conf(),
        # 创建task时的默认参数
        "job_defaults": {
            'coalesce': settings.TASK_COALESCE,
            'max_instances': settings.TASK_MAX_INSTANCES,
        }
    }

    return end_conf


# 调度器
scheduler = BackgroundScheduler(**task_conf())

__all__ = ['scheduler']
