#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import Any, Callable

import orjson
from tenacity import retry, stop_after_attempt

from backend.ninja_xia.utils.api_test.http_client import HttpClient
from backend.ninja_xia.utils.api_test.assert_control import exec_assert
from backend.ninja_xia.utils.api_test.parse_request_body import request_body_parser
from backend.xia.common.log import log
from backend.xia.models import ApiTestCase


class HttpTestCaseRunner:
    """
    Http测试用例运行器
    """

    def __init__(self, test_case, retry_num, runner):
        """
        初始化变量

        :param test_case:
        :param runner:
        :param retry_num:
        """
        self.http_client: HttpClient = HttpClient()
        self.test_case: ApiTestCase = test_case
        self.retry_num: int = retry_num
        self.runner: Any = runner or 0  # 0: 任务自动创建
        self.run: Callable = retry(stop=stop_after_attempt(self.retry_num))(self.run)

    def run(self):
        """
        运行程序

        :return:
        """
        if self.test_case is None:
            raise RuntimeError('测试用例为空')

        # 请求参数
        name = self.test_case.name
        method = self.test_case.method
        url = self.test_case.api_environment.host + self.test_case.path
        params = self.test_case.params
        headers = self.test_case.headers
        cookies = self.test_case.cookies
        body_type = self.test_case.body_type
        body = self.test_case.body
        assert_text = self.test_case.assert_text
        timeout = self.test_case.timeout

        # 获取请求数据
        request_kwargs = request_body_parser(
            params=params,
            cookies=cookies,
            headers=headers,
            body_type=body_type,
            body=body
        )
        request_kwargs.update({'timeout': timeout})

        # 发起请求
        try:
            response = self.http_client.send_request(method=method, url=url, **request_kwargs)
        except Exception as e:
            raise RuntimeError(e)
        else:
            # 记录响应结果
            response_result_list = {
                'json': orjson.loads(response['json']),
                'content': orjson.loads(response['content']),
                'text': orjson.loads(response['text']),
                'cookies': response['cookies'],
            }
            try:
                # 断言
                if assert_text:
                    assert_status = exec_assert(response, assert_text)
                    if assert_status != 'PASS':
                        log.warning('用例运行未通过, 断言结果: {}'.format(''.join(assert_status.split(',')[-1:])))
                else:
                    assert_status = '未添加断言'
            except Exception as e:
                raise RuntimeError(e)
            else:
                test_case_result = {
                    'name': name,
                    'url': url,
                    'method': method,
                    'params': params,
                    'headers': headers,
                    'body': body,
                    'status_code': response['status_code'],
                    'response_data': json.dumps(response_result_list, ensure_ascii=False),
                    'execute_time': response["stat"]["execute_time"],
                    'elapsed': response['elapsed'],
                    'assert_result': assert_status,
                    'run_status': 'PASS' if int(response['status_code']) == 200 else 'FAIL',
                    'api_case': self.test_case,
                    'api_report': None,
                    'create_user': self.runner,
                }
                return test_case_result
