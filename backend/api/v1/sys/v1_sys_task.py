#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Router

from backend.api.jwt_security import GetCurrentIsSuperuser, GetCurrentUser
from backend.common.log import log
from backend.common.task import scheduler
from backend.crud.crud_api_test.crud_api_test_task import crud_api_test_task
from backend.schemas import Response404, Response200

v1_sys_task = Router()


@v1_sys_task.get('/enable', summary='获取所有已开启的任务', auth=GetCurrentUser())
def get_all_running_tasks(request):
    tasks = []
    for job in scheduler.get_jobs():
        tasks.append({
            "id": job.id,
            "func_name": job.func_ref,
            "func": job.func,
            "trigger": str(job.trigger),
            "executor": job.executor,
            "args": job.args,
            "kwargs": job.kwargs,
            "name": job.name,
            "misfire_grace_time": job.misfire_grace_time,
            "coalesce": job.coalesce,
            "max_instances": job.max_instances,
            "next_run_time": job.next_run_time,
        })
    return Response200(data=tasks)


@v1_sys_task.post('/{module}/{pk}/run', summary='立即执行任务', auth=GetCurrentIsSuperuser())
def start_task(request, module: str, pk):
    job = scheduler.get_job(job_id=str(pk))
    if module == 'sys':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.modify_job(job_id=f'sys_{pk}', next_run_time=datetime.datetime.now())
    if module == 'api_test':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.modify_job(job_id=f'api_test_{pk}', next_run_time=datetime.datetime.now())
    else:
        return Response404(msg=f'不存在的模块 {module}')
    return Response200()


@v1_sys_task.post('/{module}/{pk}/pause', summary='暂停任务', auth=GetCurrentIsSuperuser())
def pause_task(request, module: str, pk):
    job = scheduler.get_job(job_id=str(pk))
    if module == 'sys':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.pause_job(job_id=f'sys_{pk}')
    if module == 'api_test':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.pause_job(job_id=f'api_test_{pk}')
        try:
            api_test_task = crud_api_test_task.get_task_by_id(pk)
        except Exception as e:
            log.warning('此任务的所属案例已不存在, 建议删除此任务 {}', e)
        else:
            api_test_task.state = 3
            api_test_task.save()
    else:
        return Response404(msg=f'不存在的模块 {module}')
    return Response200()


@v1_sys_task.post('/{module}/{pk}/recover', summary='恢复任务', auth=GetCurrentIsSuperuser())
def recover_task(request, module: str, pk):
    job = scheduler.get_job(job_id=str(pk))
    if module == 'sys':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.resume_job(job_id=f'sys_{pk}')
    if module == 'api_test':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.resume_job(job_id=f'api_test_{pk}')
        try:
            api_test_task = crud_api_test_task.get_task_by_id(pk)
        except Exception as e:
            log.warning('此任务的所属案例已不存在, 建议删除此任务 {}', e)
        else:
            api_test_task.state = 1
            api_test_task.save()
    else:
        return Response404(msg=f'不存在的模块 {module}')
    return Response200()


@v1_sys_task.delete('/{module}/{pk}', summary='删除任务', auth=GetCurrentIsSuperuser())
def delete_sys_task(request, module: str, pk):
    job = scheduler.get_job(job_id=str(pk))
    if module == 'sys':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.remove_job(job_id=f'sys_{pk}')
    if module == 'api_test':
        if not job:
            return Response404(msg=f'任务不存在')
        scheduler.remove_job(job_id=f'api_test_{pk}')
        try:
            api_test_task = crud_api_test_task.get_task_by_id(pk)
        except Exception as e:
            log.warning('此任务的所属案例已不存在, 建议删除此任务 {}', e)
        else:
            api_test_task.state = 0
            api_test_task.save()
    else:
        return Response404(msg=f'不存在的模块 {module}')
    return Response200()
