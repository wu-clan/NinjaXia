#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.api_test import project_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.api_test.module import GetAllApiTestModules
from backend.xia.schemas.api_test.project import GetAllApiTestProjects, CreateApiTestProject, \
    UpdateApiTestProject
from backend.xia.schemas.api_test.task import GetAllApiTestTasks

v1_api_test_project = Router()


@v1_api_test_project.get('', summary='获取所有项目', response=List[GetAllApiTestProjects], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_project(request):
    return project_service.get_all_projects()


@v1_api_test_project.get('/enable', summary='获取所有已启用项目', response=List[GetAllApiTestProjects],
                         auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_enable_project(request):
    return project_service.get_all_open_projects()


@v1_api_test_project.get('/{int:pk}', summary='获取单个项目', auth=GetCurrentUser())
def get_one_project(request, pk: int):
    project = project_service.get_project(pk)
    return response_base.response_200(data=project, exclude={'_state'})


@v1_api_test_project.post('', summary='创建项目', auth=GetCurrentIsSuperuser())
def create_project(request, obj: CreateApiTestProject):
    project_service.create(request=request, obj=obj)
    return response_base.response_200()


@v1_api_test_project.put('/{int:pk}', summary='更新项目', auth=GetCurrentIsSuperuser())
def update_project(request, pk: int, obj: UpdateApiTestProject):
    count = project_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_project.delete('/{int:pk}', summary='删除项目', auth=GetCurrentIsSuperuser())
def delete_project(request, pk: int):
    count = project_service.delete(pk=pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_project.get('/{int:pk}/modules', summary='获取单个项目所有模块', response=List[GetAllApiTestModules],
                         auth=GetCurrentUser())
@paginate(CustomPagination)
def get_project_modules(request, pk: int):
    return project_service.get_project_modules(pk)


@v1_api_test_project.get('/{pk}/tasks', summary='获取单个项目所有任务', response=List[GetAllApiTestTasks],
                         auth=GetCurrentUser())
@paginate(CustomPagination)
def get_project_tasks(request, pk: int):
    return project_service.get_project_tasks(pk)
