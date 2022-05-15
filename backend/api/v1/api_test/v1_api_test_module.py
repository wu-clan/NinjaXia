#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_module import crud_api_test_module
from backend.crud.v1.crud_api_test.crud_api_test_project import crud_api_test_project
from backend.schemas import Response200, Response403, Response404
from backend.schemas.v1.sm_api_test.sm_api_test_module import GetAllApiTestModules, CreateApiTestModule, \
    UpdateApiTestModule
from backend.utils.serialize_data import serialize_data

v1_api_test_module = Router()


@v1_api_test_module.get('/all', summary='获取所有模块', response=List[GetAllApiTestModules])
@paginate(CustomPagination)
def get_all_modules(request) -> Any:
    return crud_api_test_module.get_all_modules()


@v1_api_test_module.get('/{int:pk}', summary='获取单个模块')
def get_one_module(request, pk: int) -> Any:
    module = crud_api_test_module.get_module_by_id(pk)
    if not module:
        return Response404(msg='模块不存在')
    return Response200(data=serialize_data(module))


@v1_api_test_module.post('/create', summary='创建模块')
def create_module(request, obj: CreateApiTestModule) -> Any:
    if crud_api_test_module.get_module_by_name(obj.name):
        return Response403(msg='模块已存在, 请更改模块名称')
    try:
        _project = crud_api_test_project.get_project_by_id(obj.api_project)
    except Http404:
        raise Http404("未找到项目")
    obj.api_project = _project
    module = crud_api_test_module.create_module(obj)
    return Response200(data=serialize_data(module))


@v1_api_test_module.put('/update/{pk}', summary='更新模块')
def update_module(request, pk: int, obj: UpdateApiTestModule) -> Any:
    if not crud_api_test_module.get_module_by_id(pk):
        return Response404(msg='模块不存在')
    current_name = crud_api_test_module.get_module_name_by_id(pk)
    if not current_name == obj.name:
        if crud_api_test_module.get_module_by_name(obj.name):
            return Response403(msg='模块已存在，请更改模块名称')
    try:
        _project = crud_api_test_project.get_project_by_id(obj.api_project)
    except Http404:
        raise Http404("未找到项目")
    obj.api_project = _project
    module = crud_api_test_module.update_module(pk, obj)
    return Response200(data=serialize_data(module))


@v1_api_test_module.delete('/delete/{pk}', summary='删除模块')
def delete_module(request, pk: int) -> Any:
    try:
        module = crud_api_test_module.delete_module(pk)
    except Http404:
        raise Http404("未找到模块")
    return Response200(data=serialize_data(module))
