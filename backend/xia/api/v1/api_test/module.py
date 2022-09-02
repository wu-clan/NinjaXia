#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import Response404, Response403, Response200
from backend.xia.common.security.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.crud.api_test.module import ApiTestModuleDao
from backend.xia.crud.api_test.project import ApiTestProjectDao
from backend.xia.schemas.api_test.case import GetAllApiTestCases
from backend.xia.schemas.api_test.module import GetAllApiTestModules, CreateApiTestModule, \
    UpdateApiTestModule, ApiTestModuleResponse

v1_api_test_module = Router()


@v1_api_test_module.get('', summary='获取所有模块', response=List[GetAllApiTestModules], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_modules(request) -> Any:
    return ApiTestModuleDao.get_all_modules()


@v1_api_test_module.get('/{int:pk}', summary='获取单个模块', auth=GetCurrentUser())
def get_one_module(request, pk: int) -> Any:
    module = ApiTestModuleDao.get_one_module(pk)
    if not module:
        return Response404(msg='模块不存在')
    return ApiTestModuleResponse(data=module)


@v1_api_test_module.post('', summary='创建模块', auth=GetCurrentIsSuperuser())
def create_module(request, obj: CreateApiTestModule) -> Any:
    if ApiTestModuleDao.get_module_by_name(obj.name):
        return Response403(msg='模块已存在, 请更改模块名称')
    try:
        _project = ApiTestProjectDao.get_project_or_404(obj.api_project)
    except Http404:
        raise Http404("未找到项目")
    if not _project.status:
        return Response403(msg='所选项目已停用, 请选择其他项目')
    obj.api_project = _project
    module = ApiTestModuleDao.create_module(obj)
    module.creator = request.session['username']
    module.save()
    return ApiTestModuleResponse(data=module)


@v1_api_test_module.put('/{int:pk}', summary='更新模块', auth=GetCurrentIsSuperuser())
def update_module(request, pk: int, obj: UpdateApiTestModule) -> Any:
    if not ApiTestModuleDao.get_module_by_id(pk):
        return Response404(msg='模块不存在')
    current_name = ApiTestModuleDao.get_module_name_by_id(pk)
    if not current_name == obj.name:
        if ApiTestModuleDao.get_module_by_name(obj.name):
            return Response403(msg='模块已存在，请更改模块名称')
    try:
        _project = ApiTestProjectDao.get_project_or_404(obj.api_project)
    except Http404:
        raise Http404("未找到项目")
    if not _project.status:
        return Response403(msg='所选项目已停用, 请选择其他项目')
    obj.api_project = _project
    module = ApiTestModuleDao.update_module(pk, obj)
    module.modifier = request.session['username']
    module.save()
    return ApiTestModuleResponse(data=module)


@v1_api_test_module.delete('/{int:pk}', summary='删除模块', auth=GetCurrentIsSuperuser())
def delete_module(request, pk: int) -> Any:
    try:
        ApiTestModuleDao.delete_module(pk)
    except Http404:
        raise Http404("未找到模块")
    return Response200()


@v1_api_test_module.get('/{int:pk}/cases', response=List[GetAllApiTestCases], summary='获取单个模块所有用例',
                        auth=GetCurrentUser())
@paginate(CustomPagination)
def get_one_module_cases(request, pk: int):
    try:
        _module = ApiTestModuleDao.get_module_or_404(pk)
    except Http404:
        raise Http404("没有此模块")
    cases = ApiTestModuleDao.get_module_cases(pk)
    return cases
