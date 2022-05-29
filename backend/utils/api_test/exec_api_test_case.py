#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading

from backend.crud.crud_api_test.crud_api_test_report import crud_api_test_report_detail, crud_api_test_report
from backend.utils.api_test.http_client import HttpClient
from backend.utils.api_test.http_test_case_runner import HttpTestCaseRunner
from backend.utils.send_report import send_test_report


def exec_api_test_cases(task=None, test_cases=None, retry_num=None, runner=None):
    """
    执行 api 测试用例

    :param task:
    :param test_cases:
    :param retry_num:
    :param runner:
    :return:
    """
    test_case_result_list = []
    for test_case in test_cases:
        # 实例化http请求客户端
        http_client = HttpClient()
        # 实例化运行器
        runner = HttpTestCaseRunner(http_client=http_client, test_case=test_case, retry_num=retry_num, runner=runner)
        # 运行测试用例
        test_case_result = runner.run()
        test_case_result_list.append(test_case_result)
    # 简略报告
    case_sum = len(test_cases)
    success_sum = 0
    for _tcr in test_case_result_list:
        if _tcr.run_status == 'PASS':
            success_sum += 1
    fail_sum = case_sum - success_sum
    report = {
        'name': task.name,
        'case_num': case_sum,
        'success_num': success_sum,
        'fail_num': fail_sum,
        'api_task': task,
    }
    # 创建简略报告
    task_report = crud_api_test_report.create_report(report)
    # 批量创建测试报告详情
    for _tcr in test_case_result_list:
        _tcr.api_task_report = task_report
    crud_api_test_report_detail.create_report_detail_list(test_case_result_list)


def thread_exec_api_test_cases(task=None, test_cases=None, retry_num=None, runner=None, send_report=None):
    """
    多线程执行 api 测试用例

    :param task:
    :param test_cases:
    :param runner:
    :param retry_num:
    :param send_report:
    :return:
    """
    # 更新任务状态
    task.state = 2
    task.save()
    # 创建线程
    threads = []
    t = threading.Thread(target=exec_api_test_cases, args=(task, test_cases, retry_num, runner))
    threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    # 更新任务状态
    task.state = 1
    task.save()
    # 发送测试报告
    if send_report:
        send_test_report()
