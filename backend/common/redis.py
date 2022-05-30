#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from django_redis import get_redis_connection
from redis import Redis, TimeoutError, AuthenticationError

from backend.common.log import log


class RedisCli:

    def __init__(self):
        self.redis = get_redis_connection()

    def get_redis(self) -> Redis:
        """
        获取redis连接

        :return:
        """
        with self.redis as redis:
            return redis

    @staticmethod
    def init_redis_connect():
        """
        触发初始化连接

        :return:
        """
        try:
            redis_client.ping()
        except TimeoutError as e:
            log.error("连接redis超时 {}", e)
            sys.exit()
        except AuthenticationError as e:
            log.error("连接redis认证失败 {}", e)
            sys.exit()
        except Exception as e:
            log.error('连接redis异常 {}', e)
            sys.exit()


# 获取redis连接
redis_client = RedisCli().get_redis()
