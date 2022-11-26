#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.sys import task_service
from backend.xia.common.response.response_schema import response_base
from backend.xia.enums.task.module import TaskType

v1_sys_task = Router()


@v1_sys_task.get('/register', summary='获取所有已注册的任务', auth=GetCurrentUser())
def get_all_running_tasks(request):
    tasks = task_service.get_running_tasks()
    return response_base.response_200(data=tasks, is_queryset=True)


@v1_sys_task.post('/{module}/{pk}/run', summary='立即执行任务', auth=GetCurrentIsSuperuser())
def run_task_now(request, module: TaskType, pk: int):
    count = task_service.run(request=request, module=module, pk=pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_task.post('/{module}/{pk}/pause', summary='暂停任务', auth=GetCurrentIsSuperuser())
def pause_task(request, module: TaskType, pk: int):
    count = task_service.pause(request=request, module=module, pk=pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_task.post('/{module}/{pk}/recover', summary='恢复任务', auth=GetCurrentIsSuperuser())
def recover_task(request, module: TaskType, pk: int):
    count = task_service.recover(request=request, module=module, pk=pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()
