#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.api_test import task_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.api_test.task import GetAllApiTestTasks, CreateApiTestTask, UpdateApiTestTask, \
    GetOneApiTestTaskResponse

v1_api_test_task = Router()


@v1_api_test_task.get('', summary='获取所有任务', response=List[GetAllApiTestTasks], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_tasks(request):
    return task_service.get_tasks()


@v1_api_test_task.get('/{int:pk}', summary='获取单个任务', response=GetOneApiTestTaskResponse, auth=GetCurrentUser())
def get_one_task(request, pk: int):
    task = task_service.get_task(pk)
    return GetOneApiTestTaskResponse(data=task)


@v1_api_test_task.post('', summary='添加任务', auth=GetCurrentIsSuperuser())
def create_task(request, obj: CreateApiTestTask):
    task_service.create(request=request, obj=obj)
    return response_base.response_200()


@v1_api_test_task.put('/{int:pk}', summary='更新任务', auth=GetCurrentIsSuperuser())
def update_task(request, pk: int, obj: UpdateApiTestTask):
    count = task_service.update(request, pk, obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_task.post('/{int:pk}/enable', summary='开启任务', auth=GetCurrentUser())
def start_task(request, pk: int):
    task_service.start(request=request, pk=pk)
    return response_base.response_200()


@v1_api_test_task.delete('/{int:pk}', summary='删除任务', auth=GetCurrentIsSuperuser())
def delete_task(request, pk: int):
    task_service.delete(pk)
    return response_base.response_200()
