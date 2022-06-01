#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.common.task import scheduler, MyCronTrigger
from backend.crud.crud_api_test.crud_api_test_business import crud_api_test_business
from backend.crud.crud_api_test.crud_api_test_case import crud_api_test_case
from backend.crud.crud_api_test.crud_api_test_project import crud_api_test_project
from backend.crud.crud_api_test.crud_api_test_task import crud_api_test_task
from backend.crud.crud_sys.crud_sys_crontab import crud_crontab
from backend.schemas import Response200, Response403, Response404
from backend.schemas.sm_api_test.sm_api_test_task import GetAllApiTestTasks, CreateApiTestTask, ApiTestTaskResponse, \
    UpdateApiTestTask
from backend.utils.api_test.exec_api_test_case import thread_exec_api_test_cases

v1_api_test_task = Router()


@v1_api_test_task.get('', summary='获取所有任务', response=List[GetAllApiTestTasks], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_tasks(request):
    tasks = crud_api_test_task.get_all_tasks()
    for task in tasks:
        job = scheduler.get_job(f'api_test_{task.id}')
        if not job:
            task.state = 0
            task.save()
        if job:
            if not job.next_run_time:
                task.state = 3
                task.save()
    return tasks


@v1_api_test_task.post('', summary='添加任务', auth=GetCurrentIsSuperuser())
def create_task(request, obj: CreateApiTestTask):
    name = crud_api_test_task.get_task_by_name(obj.name)
    if name:
        return Response403(msg='任务已存在, 请更改任务名称')
    if len(obj.api_case) != 0:
        for _case in set(obj.api_case):
            case = crud_api_test_case.get_case_by_id(_case)
            if not case:
                return Response404(msg=f'用例 {case} 不存在')
    cron = crud_crontab.get_crontab_by_id(obj.sys_cron)
    if not cron:
        return Response404(msg=f'定时任务不存在')
    project = crud_api_test_project.get_project_by_id(obj.api_project)
    if not project:
        return Response404(msg=f'项目不存在')
    if not project.status:
        return Response403(msg=f'项目 {project.name} 已停用')
    business_test = crud_api_test_business.get_business_by_id(obj.api_business_test)
    if not business_test:
        return Response404(msg=f'业务测试不存在')
    obj.sys_cron = cron
    obj.api_project = project
    obj.api_business_test = business_test
    obj.api_case = ','.join(str(_) for _ in obj.api_case)
    task = crud_api_test_task.create_task(obj)
    task.creator = request.session['username']
    task.save()
    return ApiTestTaskResponse(data=task)


@v1_api_test_task.put('/{int:pk}', summary='更新任务', auth=GetCurrentIsSuperuser())
def update_task(request, pk: int, obj: UpdateApiTestTask):
    _task = crud_api_test_task.get_task_by_id(pk)
    if not _task:
        return Response404(msg=f'任务不存在')
    # 判断任务是否已开启
    if scheduler.get_job(job_id=f'api_test_{pk}'):
        return Response403(msg='任务已开启, 不支持更新')
    current_name = _task.name
    if current_name != obj.name:
        name = crud_api_test_task.get_task_by_name(obj.name)
        if name:
            return Response403(msg='任务已存在, 请更改任务名称')
    cron = crud_crontab.get_crontab_by_id(obj.sys_cron)
    if not cron:
        return Response404(msg=f'定时任务不存在')
    if len(obj.api_case) != 0:
        for _case in set(obj.api_case):
            case = crud_api_test_case.get_case_by_id(_case)
            if not case:
                return Response404(msg=f'用例 {case} 不存在')
    project = crud_api_test_project.get_project_by_id(obj.api_project)
    if not project:
        return Response404(msg=f'项目不存在')
    if not project.status:
        return Response403(msg=f'项目 {project.name} 已停用')
    business_test = crud_api_test_business.get_business_by_id(obj.api_business_test)
    if not business_test:
        return Response404(msg=f'业务测试不存在')
    obj.sys_cron = cron
    obj.api_project = project
    obj.api_business_test = business_test
    obj.api_case = ','.join(str(_) for _ in obj.api_case)
    task = crud_api_test_task.update_task(pk, obj)
    task.modifier = request.session['username']
    task.save()
    # 同时更新任务
    # if scheduler.get_job(job_id=f'api_test_{pk}'):
    #     corn = crud_crontab.format_crontab(task.sys_cron.id)
    #     scheduler.modify_job(trigger=MyCronTrigger.from_crontab(corn), job_id=f'api_test_{pk}', name=task.name)
    return ApiTestTaskResponse(data=task)


@v1_api_test_task.post('/{int:pk}/enable', summary='开启任务', auth=GetCurrentUser())
def run_async_task(request, pk: int):
    task = crud_api_test_task.get_task_by_id(pk)
    if not task:
        return Response404(msg=f'任务不存在')
    if not task.status:
        return Response403(msg='任务已停用, 不支持启动')
    if task.state != 0:
        return Response403(msg='任务已执行, 不支持重复执行')
    if not task.api_project:
        return Response404(msg=f'项目不存在')
    if not task.api_project.status:
        return Response403(msg=f'项目 {task.api_project.name} 已停用')
    if not task.sys_cron:
        return Response404(msg=f'定时器不存在')
    if task.execute_target == 0:
        cases = crud_api_test_business.get_business_cases(task.api_business_test)
    elif task.execute_target == 1:
        if len(task.api_case) == 0:
            return Response403(msg='选择执行目标为用例, 但未选择用例')
        cases = []
        cases_id = list(map(int, task.api_case.split(',')))
        for _case in cases_id:
            case = crud_api_test_case.get_case_by_id(_case)
            if not case:
                return Response404(msg=f'用例 {case} 不存在')
            cases.append(case)
    else:
        return Response403(msg='执行目标错误')
    if not cases:
        return Response403(msg='此任务不包含用例, 不支持开启')
    corn = crud_crontab.format_crontab(task.sys_cron.id)
    # 创建任务
    scheduler.add_job(func=thread_exec_api_test_cases, trigger=MyCronTrigger.from_crontab(corn),
                      args=[task, cases, task.retry_num, None, task.send_report], id=f'api_test_{pk}', name=task.name,
                      start_date=task.start_data, end_date=task.end_date)
    task.state = 1
    task.save()
    return Response200()


@v1_api_test_task.delete('/{int:pk}', summary='删除任务', auth=GetCurrentIsSuperuser())
def delete_task(request, pk: int):
    task = crud_api_test_task.get_task_by_id(pk)
    if not task:
        return Response404(msg='任务不存在')
    crud_api_test_task.delete_task(pk)
    job = scheduler.get_job(job_id=f'api_test_{pk}')
    if job:
        job.remove()
    return Response200()
