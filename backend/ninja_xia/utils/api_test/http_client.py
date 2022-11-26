#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import JSONDecodeError
from typing import Any

import httpx
from django.utils import timezone
from orjson import orjson

from backend.ninja_xia import settings
from backend.xia.common.log import log


class HttpClient:
    """
    Http请求客户端
    """

    @staticmethod
    def __init_response_meta_data() -> dict:
        """
        初始化响应元数据
        """
        response_meta_data = {
            "url": None,
            "status_code": 200,
            "elapsed": 0,
            "headers": None,
            "cookies": None,
            "json": None,
            "content": None,
            "text": None,
            "stat": {
                "execute_time": None,
            }
        }
        return response_meta_data

    @staticmethod
    def _httpx_engin(method, url, **kwargs) -> Any:
        """
        httpx 引擎

        :return:
        """
        try:
            with httpx.Client(
                    verify=settings.VERIFY,
                    follow_redirects=settings.FOLLOW_REDIRECTS,
                    proxies=settings.PROXIES
            ) as client:
                response = client.request(method=method, url=url, **kwargs)
                response.raise_for_status()
        except httpx.RequestError as e:
            log.error(f"请求 {e.request.url!r} 时出错: {e}")
            raise RuntimeError(f"请求 {e.request.url!r} 时出错: {e}")
        except httpx.HTTPStatusError as e:
            log.error(f"错误响应 {e}")
            raise RuntimeError(f"错误响应 {e}")
        except Exception as e:
            log.error(f'发送请求异常: {e}')
            raise RuntimeError(f'发送请求异常: {e}')

        return response

    def send_request(self, method, url, **kwargs) -> dict:
        """
        发送请求

        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        # 初始化响应元数据
        meta_data = self.__init_response_meta_data()

        # 执行时间
        meta_data["stat"]['execute_time'] = timezone.now()

        # 发送请求
        response = self._httpx_engin(method=method, url=url, **kwargs)

        # 记录响应的信息
        meta_data['url'] = str(response.url)
        meta_data['status_code'] = int(response.status_code)
        meta_data['elapsed'] = response.elapsed.microseconds / 1000.0
        meta_data['headers'] = dict(response.headers)
        meta_data['cookies'] = dict(response.cookies)
        try:
            json_data = response.json()
        except JSONDecodeError:
            json_data = {}
        meta_data['json'] = orjson.dumps(json_data)
        meta_data['content'] = response.content.decode('utf-8')
        meta_data['text'] = response.text

        return meta_data
