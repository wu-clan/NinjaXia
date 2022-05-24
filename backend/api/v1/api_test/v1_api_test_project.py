#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentIsSuperuser, GetCurrentUser
from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_project import crud_api_test_project
from backend.schemas import Response200, Response403
from backend.schemas.sm_api_test.sm_api_test_project import GetAllApiTestProjects, CreateApiTestProject, \
    UpdateApiTestProject
from backend.utils.serializers import serialize_data

v1_api_test_project = Router()


@v1_api_test_project.get('', summary='获取所有项目', response=List[GetAllApiTestProjects], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_project(request) -> Any:
    return crud_api_test_project.get_all_projects()


@v1_api_test_project.get('/enable', summary='获取所有已启用项目', response=List[GetAllApiTestProjects], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_enable_project(request) -> Any:
    return crud_api_test_project.get_all_enable_projects()


@v1_api_test_project.get('/{int:pk}', summary='获取单个项目', auth=GetCurrentUser())
def get_one_project(request, pk: int) -> Any:
    try:
        _project = crud_api_test_project.get_project_by_id(pk)
    except Http404:
        raise Http404("未找到项目")
    return Response200(data=serialize_data(_project))


@v1_api_test_project.post('', summary='添加项目', auth=GetCurrentIsSuperuser())
def create_project(request, obj: CreateApiTestProject) -> Any:
    if crud_api_test_project.get_project_by_name(obj.name):
        return Response403(msg='项目已存在，请更改项目名称')
    _project = crud_api_test_project.create_project(obj)
    _project.creator = request.session['username']
    _project.save()
    return Response200(data=serialize_data(_project))


@v1_api_test_project.put('/{int:pk}', summary='更新项目', auth=GetCurrentIsSuperuser())
def update_project(request, pk: int, obj: UpdateApiTestProject) -> Any:
    try:
        _project = crud_api_test_project.get_project_by_id(pk)
    except Http404:
        raise Http404("未找到项目")
    current_name = crud_api_test_project.get_project_name_by_id(pk)
    if not current_name == obj.name:
        if crud_api_test_project.get_project_by_name(obj.name):
            return Response403(msg='项目已存在，请更改项目名称')
    _project = crud_api_test_project.update_project(pk, obj)
    _project.modifier = request.session['username']
    _project.save()
    return Response200(data=serialize_data(_project))


@v1_api_test_project.delete('/{int:pk}', summary='删除项目', auth=GetCurrentIsSuperuser())
def delete_project(request, pk: int) -> Any:
    try:
        _project = crud_api_test_project.delete_project(pk)
    except Http404:
        raise Http404("未找到项目")
    return Response200(data=serialize_data(_project))


@v1_api_test_project.get('/{int:pk}/modules', summary='获取单个项目所有模块', auth=GetCurrentUser())
def get_project_modules(request, pk: int) -> Any:
    try:
        _project = crud_api_test_project.get_project_by_id(pk)
    except Http404:
        raise Http404("未找到项目")
    project_modules = crud_api_test_project.get_project_modules(pk)
    return Response200(data=serialize_data(project_modules))
