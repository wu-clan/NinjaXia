#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_project import crud_project
from backend.schemas import Response200, Response403
from backend.schemas.sm_api_test.sm_api_test_project import ProjectBase, GetProject

project = Router()


@project.get('/all', summary='获取所有项目', response=List[GetProject])
@paginate(CustomPagination)
def get_all_project(request):
    return crud_project.get_all_projects()


@project.get('/project/{pid}', summary='获取单个项目')
def get_one_project(request, pid: int) -> Any:
    try:
        _project = crud_project.get_project_by_id(pid)
    except Http404:
        raise Http404("未找到项目")
    return _project


@project.post('/add', summary='添加项目')
def add_project(request, obj: ProjectBase) -> Any:
    if not crud_project.get_project_by_name(obj.name):
        crud_project.create_project(obj)
        return Response200(data=obj)
    return Response403(msg='项目已存在，请更改项目名称')


@project.put('/update/{pid}', summary='更新项目')
def update_project(request, pid: int, obj: ProjectBase) -> Any:
    try:
        _project = crud_project.get_project_by_id(pid)
    except Http404:
        raise Http404("未找到项目")
    current_name = crud_project.get_project_name_by_id(pid)
    if not current_name == obj.name:
        if crud_project.get_project_by_name(obj.name):
            return Response403(msg='项目已存在，请更改项目名称')
    crud_project.update_project(pid, obj)
    return Response200(data=obj)


@project.delete('/delete/{pid}', summary='删除项目')
def delete_project(request, pid: int) -> Any:
    try:
        _project = crud_project.get_project_by_id(pid)
    except Http404:
        raise Http404("未找到项目")
    crud_project.delete_project(pid)
    return Response200(data=_project)
