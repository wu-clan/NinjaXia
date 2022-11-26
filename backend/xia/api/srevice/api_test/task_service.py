#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.ninja_xia.utils.api_test.exec_api_test_case import thread_exec_api_test_cases
from backend.xia.common.exception import errors
from backend.xia.common.task import scheduler, MyCronTrigger
from backend.xia.crud.api_test.business import ApiTestBusinessDao
from backend.xia.crud.api_test.case import ApiTestCaseDao
from backend.xia.crud.api_test.project import ApiTestProjectDao
from backend.xia.crud.api_test.task import ApiTestTaskDao
from backend.xia.crud.sys.crontab import SysCrontabDao
from backend.xia.enums.task.execute_target import ExecuteTargetType
from backend.xia.enums.task.state import StateType
from backend.xia.schemas.api_test.task import CreateApiTestTask, UpdateApiTestTask


def get_tasks():
    tasks = ApiTestTaskDao.get_all_tasks()
    for task in tasks:
        job = scheduler.get_job(f'api_test_{task.id}')
        if job:
            if not job.next_run_time:
                task.state = StateType.pause
                task.save()
    return tasks


def get_task(pk: int):
    task = ApiTestTaskDao.get_task_by_id(pk)
    if not task:
        raise errors.NotFoundError(msg='任务不存在')
    return ApiTestTaskDao.get_one_task(pk)


def create(*, request, obj: CreateApiTestTask):
    name = ApiTestTaskDao.get_task_by_name(obj.name)
    if name:
        raise errors.ForbiddenError(msg='任务已存在, 请更改任务名称')
    if obj.api_case is not None:
        if len(obj.api_case) != 0:
            for _case in set(obj.api_case):
                case = ApiTestCaseDao.get_case_by_id(_case)
                if not case:
                    raise errors.NotFoundError(msg=f'用例 {case} 不存在')
    cron = SysCrontabDao.get_crontab_by_id(obj.sys_cron)
    if not cron:
        raise errors.NotFoundError(msg=f'定时任务不存在')
    project = ApiTestProjectDao.get_project_by_id(obj.api_project)  # noqa
    if not project:
        raise errors.NotFoundError(msg=f'项目不存在')
    if not project.status:
        raise errors.ForbiddenError(msg=f'项目 {project.name} 已停用')
    business_test = ApiTestBusinessDao.get_business_by_id(obj.api_business_test)
    if not business_test:
        raise errors.NotFoundError(msg=f'业务测试不存在')
    obj.sys_cron = cron
    obj.api_project = project
    obj.api_business_test = business_test
    if obj.api_case is not None:
        obj.api_case = ','.join(str(_) for _ in obj.api_case)
    task = ApiTestTaskDao.create_task(obj, request.session['user'])
    return task


def update(request, pk: int, obj: UpdateApiTestTask):
    task = ApiTestTaskDao.get_task_by_id(pk)
    if not task:
        raise errors.NotFoundError(msg=f'任务不存在')
    if task.state != StateType.pause:
        raise errors.ForbiddenError(msg='任务已开启, 不支持更新')
    if task.name != obj.name:
        name = ApiTestTaskDao.get_task_by_name(obj.name)
        if name:
            raise errors.ForbiddenError(msg='任务已存在, 请更改任务名称')
    cron = SysCrontabDao.get_crontab_by_id(obj.sys_cron)
    if not cron:
        raise errors.NotFoundError(msg=f'定时任务不存在')
    case_list = []
    if obj.api_case is not None:
        if len(obj.api_case) != 0:
            for _case in set(obj.api_case):
                case = ApiTestCaseDao.get_case_by_id(_case)
                if not case:
                    raise errors.NotFoundError(msg=f'用例 {case} 不存在')
                case_list.append(case)
    project = ApiTestProjectDao.get_project_by_id(obj.api_project)  # noqa
    if not project:
        raise errors.NotFoundError(msg=f'项目不存在')
    if not project.status:
        raise errors.ForbiddenError(msg=f'项目 {project.name} 已停用')
    business_test = ApiTestBusinessDao.get_business_by_id(obj.api_business_test)
    if not business_test:
        raise errors.NotFoundError(msg=f'业务测试不存在')
    obj.sys_cron = cron
    obj.api_project = project
    obj.api_business_test = business_test
    if obj.api_case is not None:
        obj.api_case = ','.join(str(_) for _ in obj.api_case)
    count = ApiTestTaskDao.update_task(pk, obj, request.session['user'])
    # 同步更新任务
    if count > 0:
        new_task = ApiTestTaskDao.get_task_by_id(pk)
        new_case_list = []
        if obj.execute_target == ExecuteTargetType.business:
            new_case_list = ApiTestBusinessDao.get_business_case_list(obj.api_business_test)
        elif obj.execute_target == ExecuteTargetType.case:
            new_case_list = case_list
        if scheduler.get_job(job_id=f'api_test_{pk}'):
            corn = SysCrontabDao.format_crontab(task.sys_cron.id)
            scheduler.modify_job(
                job_id=f'api_test_{pk}',
                trigger=MyCronTrigger.from_crontab(corn),
                args=[new_task, new_case_list, new_task.retry_num, None, new_task.send_report],
                name=new_task.name
            )
    return count


def start(*, request, pk: int):
    if scheduler.get_job(job_id=f'api_test_{pk}'):
        raise errors.ForbiddenError(msg='任务已开启, 请勿重复操作')
    task = ApiTestTaskDao.get_task_by_id(pk)
    if not task:
        raise errors.NotFoundError(msg=f'任务不存在')
    if not task.status:
        raise errors.ForbiddenError(msg='任务已停用, 不支持开启')
    if task.state != StateType.pause:
        raise errors.ForbiddenError(msg='任务已执行, 不支持重复执行')
    if not task.api_project:
        raise errors.NotFoundError(msg=f'项目不存在')
    if not task.api_project.status:
        raise errors.ForbiddenError(msg=f'项目 {task.api_project.name} 已停用')
    if not task.sys_cron:
        raise errors.NotFoundError(msg=f'定时器不存在')
    if task.execute_target == ExecuteTargetType.business:
        case_list = ApiTestBusinessDao.get_business_case_list(task.api_business_test)
    elif task.execute_target == ExecuteTargetType.case:
        if len(task.api_case) == 0:
            raise errors.ForbiddenError(msg='选择执行目标为用例, 但未选择用例')
        case_list = []
        cases_id = list(map(int, task.api_case.split(',')))
        for _case in cases_id:
            case = ApiTestCaseDao.get_case_by_id(_case)
            if not case:
                raise errors.NotFoundError(msg=f'用例 {case} 不存在')
            case_list.append(case)
    else:
        raise errors.ForbiddenError(msg='执行目标错误')
    if not case_list:
        raise errors.ForbiddenError(msg='此任务不包含用例, 不支持开启')
    corn = SysCrontabDao.format_crontab(task.sys_cron.id)
    # 创建任务
    scheduler.add_job(
        func=thread_exec_api_test_cases,
        trigger=MyCronTrigger.from_crontab(corn),
        args=[task, case_list, task.retry_num, None, task.send_report],
        id=f'api_test_{pk}',
        name=task.name,
        start_date=task.start_datetime,
        end_date=task.end_datetime
    )
    ApiTestTaskDao.update_task_state(pk, StateType.waiting, request.session['user'])


def delete(pk: int):
    task = ApiTestTaskDao.get_task_by_id(pk)
    if not task:
        raise errors.NotFoundError(msg='任务不存在')
    ApiTestTaskDao.delete_task(pk)
    job = scheduler.get_job(job_id=f'api_test_{pk}')
    if job:
        job.remove()
