#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.api_test import case_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.enums.request.method import MethodType
from backend.xia.schemas.api_test.case import GetAllApiTestCases, CreateApiTestCase, ExtraDebugArgs, \
    GetOneApiTestCaseResponse

v1_api_test_case = Router()


@v1_api_test_case.get('', summary='获取所有用例', response=List[GetAllApiTestCases], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_cases(request):
    return case_service.get_cases()


@v1_api_test_case.get('/{pk}', summary='获取单个用例', response=GetOneApiTestCaseResponse, auth=GetCurrentUser())
def get_one_case(request, pk: int):
    case = case_service.get_case(pk)
    return GetOneApiTestCaseResponse(data=case)


@v1_api_test_case.get('/{method}/cases', summary='获取请求方式相同所有用例', response=List[GetAllApiTestCases],
                      auth=GetCurrentUser())
@paginate(CustomPagination)
def get_method_same_cases(request, method: MethodType):
    return case_service.get_cases_by_method(method=method)


@v1_api_test_case.post('', summary='新增用例', auth=GetCurrentIsSuperuser())
def create_case(request, obj: CreateApiTestCase):
    case_service.create(request=request, obj=obj)
    return response_base.response_200()


@v1_api_test_case.put('/{pk}', summary='更新用例', auth=GetCurrentIsSuperuser())
def update_case(request, pk: int, obj: CreateApiTestCase):
    count = case_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_case.delete('', summary='批量删除用例', auth=GetCurrentIsSuperuser())
def delete_cases(request, pk: List[int]):
    count = case_service.delete(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_case.post('/{pk}/debug', summary='调试用例', auth=GetCurrentUser())
def debug_case(request, pk: int, extra: ExtraDebugArgs):
    result = case_service.debug(request=request, pk=pk, extra=extra)
    return response_base.response_200(data=result)
