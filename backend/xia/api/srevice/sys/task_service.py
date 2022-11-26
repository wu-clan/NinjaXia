#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from backend.xia.common.exception import errors
from backend.xia.common.task import scheduler
from backend.xia.crud.api_test.task import ApiTestTaskDao
from backend.xia.enums.task.module import TaskType
from backend.xia.enums.task.state import StateType


def get_running_tasks():
    tasks = []
    for job in scheduler.get_jobs():
        tasks.append({
            "id": job.id,
            "func_name": job.func_ref,
            "trigger": str(job.trigger),
            "executor": job.executor,
            # "args": str(job.args),
            # "kwargs": job.kwargs,
            "name": job.name,
            "misfire_grace_time": job.misfire_grace_time,
            "coalesce": job.coalesce,
            "max_instances": job.max_instances,
            "next_run_time": job.next_run_time,
        })
    return tasks


def run(*, request, module: TaskType, pk: int):
    if module == TaskType.sys:
        job = scheduler.get_job(job_id=f'sys_{pk}')
        if not job:
            raise errors.NotFoundError(msg=f'任务不存在')
        scheduler.modify_job(job_id=f'sys_{pk}', next_run_time=datetime.now())
    if module == TaskType.api_test:
        job = scheduler.get_job(job_id=f'api_test_{pk}')
        if not job:
            raise errors.NotFoundError(msg=f'任务不存在')
        scheduler.modify_job(job_id=f'api_test_{pk}', next_run_time=datetime.now())
        count = ApiTestTaskDao.update_task_state(pk, StateType.running, request.session['user'])
        return count
    else:
        raise errors.NotFoundError(msg=f'不存在的模块 {module}')


def pause(*, request, module: TaskType, pk: int):
    if module == TaskType.sys:
        job = scheduler.get_job(job_id=f'sys_{pk}')
        if not job:
            raise errors.NotFoundError(msg=f'任务不存在')
        scheduler.pause_job(job_id=f'sys_{pk}')
    if module == TaskType.api_test:
        job = scheduler.get_job(job_id=f'api_test_{pk}')
        if not job:
            raise errors.NotFoundError(msg=f'任务不存在')
        scheduler.pause_job(job_id=f'api_test_{pk}')
        count = ApiTestTaskDao.update_task_state(pk, StateType.pause, request.session['user'])
        return count
    else:
        raise errors.NotFoundError(msg=f'不存在的模块 {module}')


def recover(*, request, module: TaskType, pk: int):
    if module == TaskType.sys:
        job = scheduler.get_job(job_id=f'sys_{pk}')
        if not job:
            raise errors.NotFoundError(msg=f'任务不存在')
        scheduler.resume_job(job_id=f'sys_{pk}')
    if module == TaskType.api_test:
        job = scheduler.get_job(job_id=f'api_test_{pk}')
        if not job:
            raise errors.NotFoundError(msg=f'任务不存在')
        scheduler.resume_job(job_id=f'api_test_{pk}')
        count = ApiTestTaskDao.update_task_state(pk, StateType.waiting, request.session['user'])
        return count
    else:
        raise errors.NotFoundError(msg=f'不存在的模块 {module}')
