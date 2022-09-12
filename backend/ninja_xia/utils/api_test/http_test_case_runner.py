#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import orjson
from tenacity import retry, stop_after_attempt

from backend.ninja_xia.utils.api_test.http_client import HttpClient
from backend.ninja_xia.utils.api_test.parse_assertions import handling_assertions
from backend.ninja_xia.utils.api_test.parse_request_body import request_body_parser
from backend.xia.common.log import log


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
        self.http_client = HttpClient()
        self.test_case = test_case
        self.retry_num = retry_num
        self.runner = runner if runner else 'timed_task'
        self.run = retry(stop=stop_after_attempt(self.retry_num))(self.run)

    def run(self):
        """
        运行程序

        :return:
        """
        if self.test_case is None:
            raise RuntimeError('测试用例为空')

        # 解析基本请求参数
        name = self.test_case.name
        method = str(self.test_case.method).upper()
        url = self.test_case.api_environment.host + self.test_case.url
        params = orjson.loads(orjson.dumps(self.test_case.params)) if self.test_case.params else None
        headers = orjson.loads(orjson.dumps(self.test_case.headers)) if self.test_case.headers else None
        cookies = orjson.loads(orjson.dumps(self.test_case.cookies)) if self.test_case.cookies else None
        body_type = self.test_case.body_type
        body = self.test_case.body
        assert_text = self.test_case.assert_text

        # 获取请求数据
        request_kwargs = {
            'params': params,
            'cookies': cookies,
            'headers': headers
        }
        body = request_body_parser(
            headers=headers,
            body_type=body_type,
            body=body
        )
        request_kwargs.update(body)
        request_kwargs.update({'timeout': self.test_case.timeout})

        # 发起请求
        try:
            response = self.http_client.send_request(method=method, url=url, **request_kwargs)
        except Exception as e:
            raise Exception(e)
        else:
            # 记录响应结果
            response_result_list = {
                "json": orjson.loads(response["response"]["json"]) if response["response"]["json"] else {},
                "content": orjson.loads(response["response"]["content"]) if response["response"]["content"] else {},
                "text": orjson.loads(response["response"]["text"]) if response["response"]["text"] else {},
                'cookies': orjson.loads(response["response"]["cookies"]) if response["response"]["cookies"] else {},
            }
            try:
                # 断言
                if assert_text:
                    assert_status = handling_assertions(response['response'], assert_text)
                    if assert_status != 'PASS':
                        log.warning('用例运行未通过, 断言结果: {}'.format(''.join(assert_status.split(',')[-1:])))
                else:
                    assert_status = '未添加断言'
            except Exception as e:
                raise Exception(e)
            else:
                # 成功下的结果
                test_case_result = {
                    'name': name,
                    'url': url,
                    'method': method,
                    'params': params,
                    'headers': headers,
                    'body': body,
                    'status_code': response['response']['status_code'],
                    'response_data': response_result_list,
                    'execute_time': response["stat"]["execute_time"],
                    'elapsed': response['response']['elapsed'],
                    'assert_result': assert_status,
                    'run_status': 'PASS' if int(response['response']['status_code']) == 200 else 'FAIL',
                    'api_case': self.test_case,
                    'api_report': None,
                    'creator': self.runner,
                }
                return test_case_result
