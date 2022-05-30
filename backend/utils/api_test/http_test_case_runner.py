#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import orjson
from django.utils import timezone
from tenacity import retry, stop_after_attempt

from backend.common.log import log
from backend.ninja_models.models.api_test.api_test_report import ApiTestReportDetail
from backend.utils.api_test.parse_assertions import handling_assertions


class StopAfter(stop_after_attempt):
    """
    重写 stop_after_attempt 类
    """
    max_attempt_number = 0

    def __init__(self) -> None:
        super().__init__(self.max_attempt_number)
        self.max_attempt_number = self.max_attempt_number


class HttpTestCaseRunner:
    """
    Http测试用例运行器
    """

    def __init__(self, http_client=None, test_case=None, retry_num=None, runner=None):
        """
        初始化变量

        :param http_client:
        :param test_case:
        :param runner:
        :param retry_num:
        """
        self.http_client = http_client
        self.test_case = test_case
        StopAfter.max_attempt_number = retry_num if retry_num else 0
        self.runner = runner if runner else '定时任务'

    @retry(stop=StopAfter())
    def run(self):
        """
        运行程序

        :return:
        """
        if self.test_case is None:
            raise RuntimeError('test_case is None')

        # 解析基本请求参数
        name = self.test_case.name
        method = str(self.test_case.method).upper() if self.test_case.method else None
        url = self.test_case.api_environment.host + self.test_case.url
        params = orjson.loads(orjson.dumps(self.test_case.params)) if self.test_case.params else {}
        headers = orjson.loads(orjson.dumps(self.test_case.headers)) if self.test_case.headers else {}
        body_type = self.test_case.body_type
        body = self.test_case.body
        assert_text = self.test_case.assert_text

        # 加固请求参数
        if len(self.test_case.headers) > 0:
            for _ in self.test_case.headers.values():
                if not isinstance(_, str):
                    raise ValueError('headers格式错误')

        # 解析请求body
        data = None
        files = None
        json = None

        if body_type == 'none':
            data = data
            files = files
            json = json
        elif body_type == 'form-data':
            data = orjson.loads(body)
        elif body_type == 'x-www-form-urlencoded':
            data = orjson.loads(body)
        elif body_type == 'binary':
            files = orjson.loads(body)
        elif body_type == 'GraphQL':
            data = orjson.loads(body)
        elif body_type == 'Text':
            pass
        elif body_type == 'JavaScript':
            pass
        elif body_type == 'JSON':
            json = orjson.loads(body)
        elif body_type == 'HTML':
            pass
        elif body_type == 'XML':
            pass
        else:
            raise ValueError('body_type错误')

        # 请求参数 end
        request_kwargs = {
            'params': params,
            'headers': headers,
            'data': data,
            'files': files,
            'json': json,
        }

        # 初期版本, 默认 timeout=10
        request_kwargs.setdefault('timeout', 10)

        # 发起请求
        execute_time = timezone.now()
        assert_status = None
        try:
            response = self.http_client.send_request(method=method, url=url, **request_kwargs)
        except Exception as e:
            # 失败情况下的结果
            test_case_result = {
                'name': name,
                'url': url,
                'method': method,
                'params': params,
                'headers': headers,
                'body': body,
                'status_code': 400,
                'response_data': e,
                'execute_time': execute_time,
                'elapsed': 0,
                'assert_result': None,
                'run_status': 'ERROR',
                'api_case': self.test_case,
                'api_report': None,
                'creator': self.runner,
            }
            return ApiTestReportDetail(**test_case_result)
        else:
            # 记录响应结果
            response_result_list = {
                "result": orjson.loads(response["response"]["result"]) if response["response"]["result"] else {},
                "content": orjson.loads(response["response"]["content"]) if response["response"]["content"] else {},
                "text": orjson.loads(response["response"]["text"]) if response["response"]["text"] else {},
                "cookies": orjson.loads(response["response"]["cookies"]) if response["response"]["cookies"] else {},
            }
            try:
                # 断言
                if assert_text:
                    assert_status = handling_assertions(response['response'], assert_text)
                    # if assert_status != 'PASS':
                    #     log.warning('用例运行未通过, 断言结果: {}'.format(''.join(assert_status.split(',')[-1:])))
            except Exception as e:
                test_case_result = {
                    'name': name,
                    'url': url,
                    'method': method,
                    'params': params,
                    'headers': headers,
                    'body': body,
                    'status_code': 400,
                    'response_data': e,
                    'execute_time': execute_time,
                    'elapsed': 0,
                    'assert_result': None,
                    'run_status': 'ERROR',
                    'api_case': self.test_case,
                    'api_report': None,
                    'creator': self.runner,
                }
                return ApiTestReportDetail(**test_case_result)
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
                    'assert_result': assert_text,
                    'run_status': assert_status,
                    'api_case': self.test_case,
                    'api_report': None,
                    'creator': self.runner,
                }
                return ApiTestReportDetail(**test_case_result)
