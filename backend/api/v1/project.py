#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.http import Http404
from ninja import Router

from backend.common.log import log
from backend.ninja_models.models.api_auto.project import ProjectCRUD
from backend.schemas import Message
from backend.schemas.project import ProjectBase, GetProject

project = Router()


@project.post('/project', summary='添加项目', response=Message)
def add_project(request, post: ProjectBase):
    if not ProjectCRUD.get_project_name(post.name):
        ProjectCRUD.add_project(post)
        log.success(f'添加项目 {post.name} 成功')
        return dict(code=200, msg='添加项目成功', data=post)
    return dict(code=403, msg='项目已存在,请更换项目名')


@project.put('/project/{pid}', summary='更新项目', response=Message)
def update_project(request, pid: int, put: ProjectBase):
    try:
        _project = ProjectCRUD.get_project_by_id(pid)
    except Http404:
        log.error('输入有误，要更新的项目不存在')
        return dict(code=404, msg='项目不存在，请重新输入')
    current_name = ProjectCRUD.get_project_name_by_id(pid)
    if not current_name == put.name:
        if ProjectCRUD.get_project_name(put.name):
            log.error(f'更新项目名 {current_name} 为 {put.name} 失败， {put.name} 项目已存在')
            return dict(code=403, msg='项目已存在，请更换项目名')
    for attr, value in put.dict().items():
        setattr(_project, attr, value)
    _project.save()
    log.success(f'更新项目 {current_name} 成功')
    return dict(code=200, msg='更新项目成功', data=put)


@project.delete('/project/{pid}', summary='删除项目', response=Message)
def delete_project(request, pid: int):
    try:
        _project = ProjectCRUD.get_project_by_id(pid)
        _name = ProjectCRUD.get_project_name_by_id(pid)
    except Http404:
        log.error('要删除的项目不存在,请重新输入')
        return dict(code=404, msg='项目不存在,请重新输入')
    _project.delete()
    log.success(f'删除项目 {_name} 成功')
    return dict(code=200, msg='删除项目成功', data=dict(name=_name))


@project.get('/project', summary='获取所有项目', response=List[GetProject])
def get_project(request, ):
    _projects = ProjectCRUD.get_all_projects()
    log.success('获取所有项目成功')
    return _projects
