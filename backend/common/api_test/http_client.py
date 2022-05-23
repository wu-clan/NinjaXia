#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from json import JSONDecodeError

import httpx
from django.utils import timezone

from backend.common.log import log


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
            "response": {
                "url": None,
                "status_code": 200,
                "elapsed": 0,
                "headers": {},
                "cookies": {},
                "result": None,
                "content": None,
                "text": None,
            },
            "stat": {
                "execute_time": None,
            }
        }
        return response_meta_data

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
        execute_time = timezone.now()
        meta_data["stat"]['execute_time'] = execute_time

        # 发送请求
        try:
            with httpx.Client(verify=False) as client:
                response = client.request(method=method, url=url, **kwargs)
                response.raise_for_status()
        except httpx.RequestError as exc:
            log.error(f"请求时出错 {exc.request.url!r}.")
            raise RuntimeError(f"请求时出错 {exc.request.url!r}.")
        except httpx.HTTPStatusError as exc:
            log.error(f"错误响应 {exc.response.status_code} 在请求 {exc.request.url!r} 时.")
            raise RuntimeError(f"错误响应 {exc.response.status_code} 在请求 {exc.request.url!r} 时.")

        # 记录响应的信息
        meta_data['response']['url'] = str(response.url)
        meta_data['response']['status_code'] = int(response.status_code)
        meta_data['response']['elapsed'] = response.elapsed.microseconds / 1000.0
        meta_data['response']['headers'] = dict(response.headers)
        meta_data['response']['cookies'] = dict(response.cookies)
        try:
            json_data = response.json()
        except JSONDecodeError:
            json_data = {}
        meta_data['response']['result'] = json.dumps(json_data)
        meta_data['response']['content'] = response.content.decode('utf-8')
        meta_data['response']['text'] = response.text

        return meta_data
