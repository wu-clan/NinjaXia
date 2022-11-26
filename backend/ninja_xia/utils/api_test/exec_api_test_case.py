#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List

import tenacity
from django.utils import timezone

from backend.ninja_xia.settings import SERVER_REPORT_PATH
from backend.ninja_xia.utils.api_test.http_test_case_runner import HttpTestCaseRunner
from backend.ninja_xia.utils.send_report.send_email import send_email_test_report
from backend.xia.common.log import log
from backend.xia.common.report import render_testcase_report_html
from backend.xia.crud.api_test.report import ApiTestReportDetailDao, ApiTestReportDao
from backend.xia.enums.task.state import StateType
from backend.xia.models import ApiTestCase
from backend.xia.models.api_test.report import ApiTestReportDetail
from backend.xia.models.api_test.task import ApiTestTask


def exec_api_test_cases(
        task: ApiTestTask,
        test_cases: List[ApiTestCase],
        retry_num: int,
        runner: int = None,
        send_report: bool = 0
):
    """
    执行 api 测试用例

    :param task:
    :param test_cases:
    :param retry_num:
    :param runner:
    :param send_report:
    :return:
    """
    test_case_result_list = []
    for test_case in test_cases:
        # 实例化运行器
        http_runner = HttpTestCaseRunner(test_case=test_case, retry_num=retry_num, runner=runner)
        # 运行测试用例
        execute_time = timezone.now()
        try:
            test_case_result = http_runner.run()
        except tenacity.RetryError as e:
            error_test_case_result = {
                'name': test_case.name,
                'url': test_case.api_environment.host + test_case.path,
                'method': test_case.method,
                'params': test_case.params,
                'headers': test_case.headers,
                'body': test_case.body,
                'status_code': 400,
                'response_data': json.dumps({'error_msg': f'{e.last_attempt.exception()}'}, ensure_ascii=False),
                'execute_time': execute_time,
                'elapsed': 0,
                'assert_result': None,
                'run_status': 'ERROR',
                'api_case': test_case,
                'api_report': None,
                'create_user': runner or 0,  # 0: 任务自动创建
            }
            test_case_result_list.append(ApiTestReportDetail(**error_test_case_result))
        else:
            test_case_result_list.append(ApiTestReportDetail(**test_case_result))
    # 创建简略报告
    total_num = len(test_cases)
    pass_num = 0
    error_num = 0
    for _tcr in test_case_result_list:
        if _tcr.run_status == 'PASS':
            pass_num += 1
        if _tcr.run_status == 'ERROR':
            error_num += 1
    fail_sum = total_num - pass_num - error_num
    report = {
        'name': task.name,
        'total_num': total_num,
        'pass_num': pass_num,
        'fail_num': fail_sum,
        'error_num': error_num,
        'api_task': task,
        'create_user': runner or 0
    }
    task_report = ApiTestReportDao.create_report(report)

    for _tcr in test_case_result_list:
        _tcr.api_report = task_report

    # 批量创建测试报告详情
    ApiTestReportDetailDao.create_report_detail_list(test_case_result_list)

    # 记录结果
    if send_report:
        elapsed = 0
        for _ in test_case_result_list:
            elapsed = elapsed + _.elapsed
        result = {
            'task_name': task.name,
            'pass_rate': '{:.2%}'.format(pass_num / total_num),
            'total': len(test_cases),
            'runner': runner or '定时任务',
            'start_time': test_case_result_list[0].execute_time,
            'elapsed': '{:.5}'.format(elapsed / 100),
            'success': pass_num,
            'failed': fail_sum,
            'error': error_num,
            'report_url': SERVER_REPORT_PATH.replace('{pk}', str(task.id)),
        }
        content = render_testcase_report_html(**result)
        return content


def thread_exec_api_test_cases(
        task: ApiTestTask,
        test_cases: List[ApiTestCase],
        retry_num: int,
        runner: int = None,
        send_report: bool = 0
):
    """
    多线程执行 api 测试用例

    :param task:
    :param test_cases:
    :param runner:
    :param retry_num:
    :param send_report:
    :return:
    """
    log.info('=> 开始执行任务：{}'.format(task.name))
    # 更新任务状态
    task.state = StateType.running
    task.save()
    try:
        # 创建线程, 暂时不使用threading.Thread
        # threads = []
        # for i in range(10):
        #     t1 = threading.Thread(target=exec_api_test_cases, args=(task, test_cases, retry_num, runner))
        #     threads.append(t1)
        #
        # for t1 in threads:
        #     t1.start()
        #
        # for t1 in threads:
        #     t1.join()
        #
        # 这里想要拿到返回值，所以使用线程池
        # 如果不这样使用,也可以修改报告model,从根本上解决数据引用问题,但是记得要把其他用到报告model的地方也进行修改
        pool = ThreadPoolExecutor(max_workers=10)
        future = pool.submit(exec_api_test_cases, task, test_cases, retry_num, runner, send_report)
        content = future.result()
        pool.shutdown()
    except Exception as e:
        log.error('多线程执行api测试用例失败: %s' % e)
        # pass
        raise e
    finally:
        # 更新任务状态
        task.state = StateType.waiting
        task.save()

    # 发送测试报告
    if send_report:
        subject = 'API测试任务【{}】测试报告'.format(task.name)

        t2 = threading.Thread(
            target=send_email_test_report,
            args=(subject, content if content else '<h1>500 Server Error</h1>')
        )
        t2.start()
        t2.join()

    log.info('=> 执行任务：{} 结束'.format(task.name))
