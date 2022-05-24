#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.common.api_test.http_client import HttpClient
from backend.common.api_test.http_test_case_debug import HttpTestCaseDebug
from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_case import crud_api_test_case
from backend.crud.crud_api_test.crud_api_test_env import crud_api_test_env
from backend.crud.crud_api_test.crud_api_test_module import crud_api_test_module
from backend.schemas import Response404, Response200, Response403
from backend.schemas.sm_api_test.sm_api_test_case import GetAllApiTestCase, CreateApiTestCase, ExtraDebugArgs
from backend.utils.serializers import serialize_data

v1_api_test_case = Router()


@v1_api_test_case.get('', summary='获取所有用例', response=List[GetAllApiTestCase], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_cases(request):
    return crud_api_test_case.get_all_cases()


@v1_api_test_case.get('/{int:pk}', summary='获取单个用例', auth=GetCurrentUser())
def get_one_case(request, pk: int):
    case = crud_api_test_case.get_case_by_id(pk)
    if not case:
        return Response404(msg='用例不存在')
    case.params = json.loads(str(case.params))
    case.headers = json.loads(str(case.headers))
    return Response200(data=serialize_data(case))


@v1_api_test_case.post('', summary='新增用例', auth=GetCurrentIsSuperuser())
def create_case(request, obj: CreateApiTestCase):
    if crud_api_test_case.get_case_by_name(obj.name):
        return Response403(msg='用例已存在, 请更换用例名称')
    _module = crud_api_test_module.get_module_by_id(obj.api_module)
    if not _module:
        return Response404(msg='模块不存在')
    _env = crud_api_test_env.get_env_by_id(obj.api_environment)
    if not _env:
        return Response404(msg='环境不存在')
    if not _env.status:
        return Response403(msg='所选环境已停用, 请选择其他环境')
    if isinstance(obj.params, dict):
        obj.params = json.dumps(obj.params, ensure_ascii=False)
    else:
        return Response403(msg='params格式错误')
    if isinstance(obj.headers, dict):
        obj.headers = json.dumps(obj.headers, ensure_ascii=False)
    else:
        return Response403(msg='headers格式错误')
    if obj.body_type == 'JSON' or obj.body_type == 'form-data' or obj.body_type == 'x-www-form-urlencoded' or \
            obj.body_type == 'binary' or obj.body_type == 'GraphQL':
        obj.body = json.dumps(obj.body, ensure_ascii=False)
    obj.api_module = _module
    obj.api_environment = _env
    case = crud_api_test_case.create_case(obj)
    case.creator = request.session['username']
    case.save()
    return Response200(data=serialize_data(case))


@v1_api_test_case.put('/{int:pk}', summary='更新用例', auth=GetCurrentIsSuperuser())
def update_case(request, pk: int, obj: CreateApiTestCase):
    case = crud_api_test_case.get_case_by_id(pk)
    if not case:
        return Response404(msg='用例不存在')
    if case.name != obj.name:
        if crud_api_test_case.get_case_by_name(obj.name):
            return Response403(msg='用例已存在, 请更换用例名称')
    _module = crud_api_test_module.get_module_by_id(obj.api_module)
    if not _module:
        return Response404(msg='模块不存在')
    _env = crud_api_test_env.get_env_by_id(obj.api_environment)
    if not _env:
        return Response404(msg='环境不存在')
    if not _env.status:
        return Response403(msg='所选环境已停用, 请选择其他环境')
    if isinstance(obj.params, dict):
        obj.params = json.dumps(obj.params, ensure_ascii=False)
    else:
        return Response403(msg='params格式错误')
    if isinstance(obj.headers, dict):
        obj.headers = json.dumps(obj.headers, ensure_ascii=False)
    else:
        return Response403(msg='headers格式错误')
    if obj.body_type == 'JSON' or obj.body_type == 'form-data' or obj.body_type == 'x-www-form-urlencoded' or \
            obj.body_type == 'binary' or obj.body_type == 'GraphQL':
        obj.body = json.dumps(obj.body, ensure_ascii=False)
    obj.api_module = _module
    obj.api_environment = _env
    case = crud_api_test_case.update_case(pk, obj)
    case.modifier = request.session['username']
    case.save()
    return Response200(data=serialize_data(case))


@v1_api_test_case.delete('', summary='批量删除用例', auth=GetCurrentIsSuperuser())
def delete_case(request, pk: List[int]):
    for i in pk:
        case = crud_api_test_case.get_case_by_id(i)
        if not case:
            return Response404(msg=f'用例 {i} 不存在')
    crud_api_test_case.delete_case(pk)
    return Response200()


@v1_api_test_case.post('/{int:pk}/debug', summary='调试用例', auth=GetCurrentUser())
def debug_case(request, pk: int, extra: ExtraDebugArgs):
    case = crud_api_test_case.get_case_by_id(pk)
    if not case:
        return Response404(msg='用例不存在')
    if not case.api_environment:
        return Response403(msg='用例未绑定环境, 请先绑定环境')
    if not case.api_environment.status:
        return Response403(msg='用例依赖环境已停用, 请更新使用环境')
    url = case.api_environment.host + case.url
    # 实例化http请求
    http_client = HttpClient()
    # 实例化请求参数
    http_test_case_debug = HttpTestCaseDebug(http_client=http_client, test_case_name=case.name, method=case.method,
                                             url=url, params=case.params, headers=case.headers, cookies=extra.cookies,
                                             body_type=case.body_type, body=case.body, assert_text=case.assert_text,
                                             timeout=extra.timeout)
    # 调试用例
    debug_result = http_test_case_debug.debug()

    # 更新结果
    debug_result.update({
        'project': case.api_module.api_project.name,
        'module': case.api_module.name,
        'environment': case.api_environment.host,
        'case': case.id,
        'case_name': case.name,
        'description': case.description,
        'executor': request.session['username'],
        'is_task': False,
    })

    return Response200(data=debug_result)
