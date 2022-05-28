#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import orjson

from backend.common.log import log
from backend.utils.api_test.parse_assertions import handling_assertions


class HttpTestCaseDebug:
    """
    Http测试用例调试
    """

    def __init__(self, http_client=None, test_case_name=None, method=None, url=None, params=None, cookies=None,
                 headers=None, body_type=None, body=None, assert_text=None, timeout=None):
        """
        构造函数

        :param http_client:
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
        self.http_client = http_client
        self.test_case_name = test_case_name
        self.method = str(method).upper() if method else None
        self.url = url
        self.params = orjson.loads(orjson.dumps(params)) if params else {}
        self.cookies = orjson.loads(orjson.dumps(cookies)) if cookies else {}
        self.headers = orjson.loads(orjson.dumps(headers)) if headers else {}
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
        log.info(f'----------------- Debugging case: {self.test_case_name} -----------------')
        log.info(f'Method: {self.method}')
        log.info(f'Url: {self.url}')
        log.info(f'Params: {self.params}')
        log.info(f'Cookies: {self.cookies}')
        log.info(f'Headers: {self.headers}')
        log.info(f'Body Type: {self.body_type}')
        log.info(f'Body: {self.body}')
        log.info(f'Assert Text: {self.assert_text}')

        # 加固请求参数
        if len(self.headers) > 0:
            for _ in self.headers.values():
                if not isinstance(_, str):
                    raise ValueError('headers格式错误')

        # 解析请求body
        data = None
        files = None
        json = None

        if self.body_type == 'none':
            data = data
            files = files
            json = json
        elif self.body_type == 'form-data':
            data = orjson.loads(self.body)
        elif self.body_type == 'x-www-form-urlencoded':
            data = orjson.loads(self.body)
        elif self.body_type == 'binary':
            files = orjson.loads(self.body)
        elif self.body_type == 'GraphQL':
            data = orjson.loads(self.body)
        elif self.body_type == 'Text':
            pass
        elif self.body_type == 'JavaScript':
            pass
        elif self.body_type == 'JSON':
            json = orjson.loads(self.body)
        elif self.body_type == 'HTML':
            pass
        elif self.body_type == 'XML':
            pass
        else:
            raise ValueError('body_type错误')

        request_kwargs = {
            'params': self.params,
            'cookies': self.cookies,
            'headers': self.headers,
            'data': data,
            'files': files,
            'json': json,
        }

        if self.timeout:
            request_kwargs.update({'timeout': self.timeout})

        # 发送请求
        response = self.http_client.send_request(method=self.method, url=self.url, **request_kwargs)

        # 记录响应结果
        response_result_list = {
            "result": orjson.loads(response["response"]["result"]) if response["response"]["result"] else {},
            "content": orjson.loads(response["response"]["content"]) if response["response"]["content"] else {},
            "text": orjson.loads(response["response"]["text"]) if response["response"]["text"] else {}
        }
        response_result = orjson.loads(orjson.dumps(response))
        log.info(f'Response: {response_result}')

        # 断言
        if self.assert_text:
            self.assert_status = handling_assertions(response['response'], self.assert_text)
            if self.assert_status != 'PASS':
                log.warning('用例调试未通过, 断言结果: {}'.format(''.join(self.assert_status.split(',')[-1:])))

        test_case_result = {
            'url': self.url,
            'method': self.method,
            'params': self.params,
            'cookies': self.cookies,
            'headers': self.headers,
            'body_type': self.body_type,
            'body': self.body,
            'status_code': response['response']['status_code'],
            'execute_time': response["stat"]["execute_time"],
            'elapsed': response['response']['elapsed'],
            'results': response_result_list,
            'assert_text': self.assert_text,
            "assert_status": self.assert_status,
        }

        return test_case_result
