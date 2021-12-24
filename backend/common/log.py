#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from loguru import logger

from backend.autoproject import settings


class Logger(object):

    @staticmethod
    def log():
        # 判定文件夹
        if not os.path.exists(settings.LOG_PATH):
            os.mkdir(settings.LOG_PATH)

        # 日志文件名称
        log_file = os.path.join(settings.LOG_PATH, "NinjaAutoTest.log")

        # loguru日志
        logger.add(
            log_file,
            level="DEBUG",
            rotation='00:00',
            retention="7 days",
            encoding='utf-8',
            enqueue=True,
            backtrace=True,
            diagnose=True
        )

        return logger


log = Logger().log()
