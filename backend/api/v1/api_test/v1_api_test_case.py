#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_case import crud_api_test_case
from backend.crud.crud_api_test.crud_api_test_env import crud_api_test_env
from backend.crud.crud_api_test.crud_api_test_module import crud_api_test_module
from backend.schemas import Response404, Response200, Response403
from backend.schemas.sm_api_test.sm_api_test_case import GetAllApiTestCase, CreateApiTestCase
from backend.utils.serialize_data import serialize_data

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
    obj.api_module = _module
    obj.api_environment = _env
    case = crud_api_test_case.create_case(obj)
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
    obj.api_module = _module
    obj.api_environment = _env
    case = crud_api_test_case.update_case(pk, obj)
    return Response200(data=serialize_data(case))


@v1_api_test_case.delete('/{int:pk}', summary='删除用例', auth=GetCurrentIsSuperuser())
def delete_case(request, pk: int):
    case = crud_api_test_case.get_case_by_id(pk)
    if not case:
        return Response404(msg='用例不存在')
    case = crud_api_test_case.delete_case(pk)
    return Response200(data=serialize_data(case))
