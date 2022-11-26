#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import Http404

from backend.xia.common.exception import errors
from backend.xia.crud.api_test.module import ApiTestModuleDao
from backend.xia.crud.api_test.project import ApiTestProjectDao
from backend.xia.schemas.api_test.module import CreateApiTestModule, UpdateApiTestModule


def get_modules():
    return ApiTestModuleDao.get_all_modules()


def get_module(pk: int):
    module = ApiTestModuleDao.get_one_module(pk)
    if not module:
        raise errors.NotFoundError(msg='模块不存在')
    return module


def create(*, request, obj: CreateApiTestModule):
    if ApiTestModuleDao.get_module_by_name(obj.name):
        raise errors.ForbiddenError(msg='模块已存在, 请更改模块名称')
    try:
        project = ApiTestProjectDao.get_project_or_404(obj.api_project)
    except Http404:
        raise errors.HTTP404("项目不存在")
    if not project.status:
        raise errors.ForbiddenError(msg='所选项目已停用, 请选择其他项目')
    obj.api_project = project
    module = ApiTestModuleDao.create_module(obj, request.session['user'])
    return module


def update(*, request, pk: int, obj: UpdateApiTestModule):
    if not ApiTestModuleDao.get_module_by_id(pk):
        raise errors.NotFoundError(msg='模块不存在')
    current_name = ApiTestModuleDao.get_module_name_by_id(pk)
    if not current_name == obj.name:
        if ApiTestModuleDao.get_module_by_name(obj.name):
            raise errors.ForbiddenError(msg='模块已存在，请更改模块名称')
    try:
        project = ApiTestProjectDao.get_project_or_404(obj.api_project)
    except Http404:
        raise errors.HTTP404("项目不存在")
    if not project.status:
        raise errors.ForbiddenError(msg='所选项目已停用, 请选择其他项目')
    obj.api_project = project
    count = ApiTestModuleDao.update_module(pk, obj, request.session['user'])
    return count


def delete(pk: int):
    module = ApiTestModuleDao.get_module_by_id(pk)
    if not module:
        raise errors.NotFoundError(msg='模块不存在')
    count = ApiTestModuleDao.delete_module(pk)
    return count


def get_module_cases(pk: int):
    try:
        _module = ApiTestModuleDao.get_module_or_404(pk)
    except Http404:
        raise Http404("没有此模块")
    cases = ApiTestModuleDao.get_module_cases(pk)
    return cases
