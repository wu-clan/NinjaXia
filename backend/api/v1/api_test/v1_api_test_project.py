#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.api.security import GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_project import crud_api_test_project
from backend.schemas import Response200, Response403
from backend.schemas.v1.sm_api_test.sm_api_test_project import ApiTestProjectBase, GetAllApiTestProjects

v1_api_test_project = Router()


@v1_api_test_project.get('/all', summary='获取所有项目', response=List[GetAllApiTestProjects])
@paginate(CustomPagination)
def get_all_project(request):
    return crud_api_test_project.get_all_projects()


@v1_api_test_project.get('/{pid}', summary='获取单个项目')
def get_one_project(request, pid: int) -> Any:
    try:
        _project = crud_api_test_project.get_project_by_id(pid)
    except Http404:
        raise Http404("未找到项目")
    return _project


@v1_api_test_project.post('/create', summary='添加项目', auth=GetCurrentIsSuperuser())
def add_project(request, obj: ApiTestProjectBase) -> Any:
    if not crud_api_test_project.get_project_by_name(obj.name):
        crud_api_test_project.create_project(obj)
        return Response200(data=obj)
    return Response403(msg='项目已存在，请更改项目名称')


@v1_api_test_project.put('/update/{pid}', summary='更新项目', auth=GetCurrentIsSuperuser())
def update_project(request, pid: int, obj: ApiTestProjectBase) -> Any:
    try:
        _project = crud_api_test_project.get_project_by_id(pid)
    except Http404:
        raise Http404("未找到项目")
    current_name = crud_api_test_project.get_project_name_by_id(pid)
    if not current_name == obj.name:
        if crud_api_test_project.get_project_by_name(obj.name):
            return Response403(msg='项目已存在，请更改项目名称')
    crud_api_test_project.update_project(pid, obj)
    return Response200(data=obj)


@v1_api_test_project.delete('/delete/{pid}', summary='删除项目', auth=GetCurrentIsSuperuser())
def delete_project(request, pid: int) -> Any:
    try:
        _project = crud_api_test_project.get_project_by_id(pid)
    except Http404:
        raise Http404("未找到项目")
    crud_api_test_project.delete_project(pid)
    return Response200(data=_project)
