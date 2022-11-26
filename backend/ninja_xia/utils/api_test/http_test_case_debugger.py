#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

import orjson

from backend.ninja_xia.utils.api_test.assert_control import exec_assert
from backend.ninja_xia.utils.api_test.http_client import HttpClient
from backend.ninja_xia.utils.api_test.parse_request_body import request_body_parser
from backend.xia.common.log import log


class HttpTestCaseDebugger:
    """
    Http测试用例调试
    """

    def __init__(
            self,
            test_case_name: str = None,
            method: str = None,
            url: str = None,
            params: str = None,
            cookies: str = None,
            headers: str = None,
            body_type: int = None,
            body: Any = None,
            assert_text: str = None,
            timeout: int = None
    ):
        """
        构造函数

        :param test_case_name:
        :param method:
        :param url:
        :param params:
        :param cookies:
        :param headers:
        :param body_type:
        :param body:
        :param assert_text:
        :param timeout:
        """
        self.http_client = HttpClient()
        self.test_case_name = test_case_name
        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.cookies = cookies
        self.body_type = body_type
        self.body = body
        self.assert_text = assert_text
        self.timeout = timeout
        self.assert_status = None

    def debug(self):
        """
        调试程序

        :return:
        """
        # 记录请求参数
        log.info(f'🧩 Debugging case: {self.test_case_name}')
        log.info(f'Method: {self.method}')
        log.info(f'Url: {self.url}')
        log.info(f'Params: {self.params}')
        log.info(f'Cookies: {self.cookies}')
        log.info(f'Headers: {self.headers}')
        log.info(f'Body Type: {self.body_type}')
        log.info(f'Body: {self.body}')
        log.info(f'Assert Text: {self.assert_text}')

        # 获取请求数据
        request_kwargs = request_body_parser(
            params=self.params,
            cookies=self.cookies,
            headers=self.headers,
            body_type=self.body_type,
            body=self.body
        )
        request_kwargs.update({'timeout': self.timeout})

        # 发送请求
        response = self.http_client.send_request(method=self.method, url=self.url, **request_kwargs)

        # 记录响应结果
        response_result_list = {
            'json': orjson.loads(response['json']),
            'content': orjson.loads(response['content']),
            'text': orjson.loads(response['text']),
            'cookies': response['cookies'],
        }

        # 断言
        if self.assert_text:
            self.assert_status = exec_assert(response, self.assert_text)
            if self.assert_status != 'PASS':
                log.warning('用例调试未通过, 断言结果: {}'.format(''.join(self.assert_status.split(',')[-1:])))

        # 测试结果
        test_case_result = {
            'url': self.url,
            'method': self.method,
            'params': self.params,
            'headers': self.headers,
            'body_type': self.body_type,
            'body': self.body,
            'status_code': response['status_code'],
            'execute_time': response["stat"]["execute_time"],
            'elapsed': response['elapsed'],
            'results': response_result_list,
            'assert_text': self.assert_text,
            "assert_status": self.assert_status,
        }

        return test_case_result
