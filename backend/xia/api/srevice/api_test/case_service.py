#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from threading import Thread
from typing import List

from backend.ninja_xia.utils.api_test.http_test_case_debugger import HttpTestCaseDebugger
from backend.xia.common.exception import errors
from backend.xia.common.log import log
from backend.xia.crud.api_test.case import ApiTestCaseDao
from backend.xia.crud.api_test.env import ApiTestEnvDao
from backend.xia.crud.api_test.module import ApiTestModuleDao
from backend.xia.crud.api_test.report import ApiTestReportDetailDao
from backend.xia.schemas.api_test.case import CreateApiTestCase, ExtraDebugArgs


def get_cases():
    return ApiTestCaseDao.get_all_cases()


def get_cases_by_method(method: str):
    return ApiTestCaseDao.get_cases_by_method(method)


def get_case(pk: int):
    case = ApiTestCaseDao.get_one_case(pk)
    if not case:
        raise errors.NotFoundError(msg='用例不存在')
    return case


def create(*, request, obj: CreateApiTestCase):
    if ApiTestCaseDao.get_case_by_name(obj.name):
        raise errors.ForbiddenError(msg='用例已存在, 请更换用例名称')
    module = ApiTestModuleDao.get_module_by_id(obj.api_module)
    if not module:
        raise errors.NotFoundError(msg='模块不存在')
    env = ApiTestEnvDao.get_env_by_id(obj.api_environment)
    if not env:
        raise errors.NotFoundError(msg='环境不存在')
    if not env.status:
        raise errors.ForbiddenError(msg='所选环境已停用, 请选择其他环境')
    obj.api_module = module
    obj.api_environment = env
    case = ApiTestCaseDao.create_case(obj, request.session['user'])
    return case


def update(*, request, pk: int, obj: CreateApiTestCase):
    case = ApiTestCaseDao.get_case_by_id(pk)
    if not case:
        raise errors.NotFoundError(msg='用例不存在')
    if case.name != obj.name:
        if ApiTestCaseDao.get_case_by_name(obj.name):
            raise errors.ForbiddenError(msg='用例已存在, 请更换用例名称')
    module = ApiTestModuleDao.get_module_by_id(obj.api_module)
    if not module:
        raise errors.NotFoundError(msg='模块不存在')
    env = ApiTestEnvDao.get_env_by_id(obj.api_environment)
    if not env:
        raise errors.NotFoundError(msg='环境不存在')
    if not env.status:
        raise errors.ForbiddenError(msg='所选环境已停用, 请选择其他环境')
    obj.api_module = module
    obj.api_environment = env
    count = ApiTestCaseDao.update_case(pk, obj, request.session['user'])
    return count


def delete(pk: List[int]):
    for i in pk:
        case = ApiTestCaseDao.get_case_by_id(i)
        if not case:
            raise errors.NotFoundError(msg=f'用例 {i} 不存在')
    count = ApiTestCaseDao.delete_cases(pk)
    return count


def debug(*, request, pk: int, extra: ExtraDebugArgs):
    case = ApiTestCaseDao.get_case_by_id(pk)
    if not case:
        raise errors.NotFoundError(msg='用例不存在')
    if not case.api_module.api_project.status:
        raise errors.ForbiddenError(msg='此用例所属项目已停用, 不支持此操作')
    if not case.api_environment:
        raise errors.ForbiddenError(msg='用例未绑定环境, 请先绑定环境')
    if not case.api_environment.status:
        raise errors.ForbiddenError(msg='用例依赖环境已停用, 请更新使用环境')
    url = case.api_environment.host + case.path
    # 实例化请求参数
    http_test_case_debug = HttpTestCaseDebugger(
        test_case_name=case.name,
        method=case.method,
        url=url,
        params=case.params,
        headers=case.headers,
        cookies=case.cookies,
        body_type=case.body_type,
        body=case.body,
        assert_text=case.assert_text,
        timeout=case.timeout
    )

    # 发送调试
    debug_result = http_test_case_debug.debug()

    # 更新结果
    debug_result.update({
        'project': case.api_module.api_project.name,
        'module': case.api_module.name,
        'environment': case.api_environment.host,
        'case': case.id,
        'case_name': case.name,
        'description': case.description,
        'executor': request.session['user'],
        'is_task': False,
    })

    # 写入测试报告
    if extra.is_write_report:
        test_case_report = {
            'name': debug_result['case_name'],
            'url': debug_result['url'],
            'method': debug_result['method'],
            'params': debug_result['params'],
            'headers': debug_result['headers'],
            'body': debug_result['body'],
            'status_code': debug_result['status_code'],
            'response_data': json.dumps(debug_result['results'], ensure_ascii=False),
            'execute_time': debug_result['execute_time'],
            'elapsed': debug_result['elapsed'],
            'assert_result': debug_result['assert_status'],
            'run_status': debug_result['assert_status'],
            'api_case': case,
            'api_report': None,
            'create_user': debug_result['executor'],
        }
        try:
            write_report = Thread(
                target=ApiTestReportDetailDao.create_report_detail,
                args=[test_case_report]
            )
            write_report.start()
            write_report.join()
        except Exception as e:
            log.error(f'write api case <{case.name}> report error, {e}')
            raise errors.ServerError(msg='写入测试报告失败')

    return debug_result
