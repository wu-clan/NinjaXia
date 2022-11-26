#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import Http404

from backend.xia.common.exception import errors
from backend.xia.common.task import scheduler
from backend.xia.crud.api_test.project import ApiTestProjectDao
from backend.xia.enums.task.state import StateType
from backend.xia.schemas.api_test.project import CreateApiTestProject, UpdateApiTestProject


def get_all_projects():
    return ApiTestProjectDao.get_all_projects()


def get_all_open_projects():
    return ApiTestProjectDao.get_all_enable_projects()


def get_project(pk: int):
    try:
        project = ApiTestProjectDao.get_project_or_404(pk)
    except Http404:
        raise errors.HTTP404('项目不存在')
    return project


def create(*, request, obj: CreateApiTestProject):
    if ApiTestProjectDao.get_project_by_name(obj.name):
        raise errors.ForbiddenError(msg='项目已存在，请更改项目名称')
    project = ApiTestProjectDao.create_project(obj, request.session['user'])
    return project


def update(*, request, pk: int, obj: UpdateApiTestProject):
    try:
        ApiTestProjectDao.get_project_or_404(pk)
    except Http404:
        raise errors.HTTP404('项目不存在')
    current_name = ApiTestProjectDao.get_project_name_by_id(pk)
    if current_name != obj.name:
        if ApiTestProjectDao.get_project_by_name(obj.name):
            raise errors.ForbiddenError(msg='项目已存在，请更改项目名称')
    count = ApiTestProjectDao.update_project(pk, obj, request.session['user'])
    return count


def delete(pk: int):
    project = ApiTestProjectDao.get_project_by_id(pk)
    if not project:
        raise errors.NotFoundError(msg='项目不存在')
    count = ApiTestProjectDao.delete_project(pk)
    return count


def get_project_modules(pk: int):
    project = ApiTestProjectDao.get_project_by_id(pk)
    if not project:
        raise errors.NotFoundError(msg='项目不存在')
    modules = ApiTestProjectDao.get_project_modules(pk)
    return modules


def get_project_tasks(pk: int):
    project = ApiTestProjectDao.get_project_by_id(pk)
    if not project:
        raise errors.NotFoundError(msg='项目不存在')
    tasks = ApiTestProjectDao.get_project_tasks(pk)
    for task in tasks:
        job = scheduler.get_job(f'api_test_{task.id}')
        if job:
            if not job.next_run_time:
                task.state = StateType.pause
                task.save()
    return tasks
