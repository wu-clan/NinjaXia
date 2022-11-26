#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.api_test import module_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.api_test.case import GetAllApiTestCases
from backend.xia.schemas.api_test.module import GetAllApiTestModules, CreateApiTestModule, \
    UpdateApiTestModule, GetOneApiTestModuleResponse

v1_api_test_module = Router()


@v1_api_test_module.get('', summary='获取所有模块', response=List[GetAllApiTestModules], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_modules(request):
    return module_service.get_modules()


@v1_api_test_module.get('/{int:pk}', summary='获取单个模块', response=GetOneApiTestModuleResponse, auth=GetCurrentUser())
def get_one_module(request, pk: int):
    model = module_service.get_module(pk)
    return GetOneApiTestModuleResponse(data=model)


@v1_api_test_module.post('', summary='创建模块', auth=GetCurrentIsSuperuser())
def create_module(request, obj: CreateApiTestModule):
    module_service.create(request=request, obj=obj)
    return response_base.response_200()


@v1_api_test_module.put('/{int:pk}', summary='更新模块', auth=GetCurrentIsSuperuser())
def update_module(request, pk: int, obj: UpdateApiTestModule):
    count = module_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_module.delete('/{int:pk}', summary='删除模块', auth=GetCurrentIsSuperuser())
def delete_module(request, pk: int):
    count = module_service.delete(pk=pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_module.get('/{int:pk}/cases', response=List[GetAllApiTestCases], summary='获取单个模块所有用例',
                        auth=GetCurrentUser())
@paginate(CustomPagination)
def get_one_module_cases(request, pk: int):
    return module_service.get_module_cases(pk)
