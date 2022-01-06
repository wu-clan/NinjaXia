#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.http import Http404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from backend.common.log import log
from backend.ninja_models.models.api_auto.project import ProjectCRUD
from backend.schemas import Message
from backend.schemas.project import ProjectBase, GetProject

project = Router()


@project.post('/project', summary='添加项目', response=Message)
def add_project(request, post: ProjectBase):
    if not ProjectCRUD.get_project_name(post.name):
        ProjectCRUD.add_project(post)
        log.success(f'add item {post.name} success')
        return dict(code=200, msg='添加项目成功', data=post)
    log.error('the project already exists, please change the project name')
    return dict(code=403, msg='项目已存在,请更换项目名')


@project.put('/project/{pid}', summary='更新项目', response=Message)
def update_project(request, pid: int, put: ProjectBase):
    try:
        _project = ProjectCRUD.get_project_by_id(pid)
    except Http404:
        log.error('input error，the item to be updated does not exist')
        return dict(code=404, msg='项目不存在，请重新输入')
    current_name = ProjectCRUD.get_project_name_by_id(pid)
    if not current_name == put.name:
        if ProjectCRUD.get_project_name(put.name):
            log.error(f'update project name {current_name} to {put.name} fail， {put.name} project already exists')
            return dict(code=403, msg='项目已存在，请更换项目名')
    for attr, value in put.dict().items():
        setattr(_project, attr, value)
    _project.save()
    log.success(f'update item {current_name} success')
    return dict(code=200, msg='更新项目成功', data=put)


@project.delete('/project/{pid}', summary='删除项目', response=Message)
def delete_project(request, pid: int):
    try:
        _project = ProjectCRUD.get_project_by_id(pid)
        _name = ProjectCRUD.get_project_name_by_id(pid)
    except Http404:
        log.error('the item to be deleted does not exist, please re-enter')
        return dict(code=404, msg='项目不存在,请重新输入')
    _project.delete()
    log.success(f'delete item {_name} success')
    return dict(code=200, msg='删除项目成功', data=dict(name=_name))


@project.get('/project', summary='获取所有项目', response=List[GetProject])
@paginate
def get_project(request, **kwargs):
    _projects = ProjectCRUD.get_all_projects()
    log.success('get all items successful')
    return _projects


@project.get('/project/{pid}', summary='获取单个项目', response=GetProject)
def get_one_project(request, pid: int):
    try:
        p = ProjectCRUD.get_project_by_id(pid)
    except Http404:
        raise HttpError(404, '没有此项目')
    log.success(f'get {pid} project successful')
    return p
