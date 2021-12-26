#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import Http404
from ninja import Router

from backend.models.project import Project, ProjectCRUD
from backend.schemas import Message
from backend.schemas.project import ProjectBase

tester = Router()


@tester.post('/project', summary='添加项目', response=Message)
def add_project(request, post: ProjectBase):
    if not ProjectCRUD.get_project_name(post):
        Project.objects.create(**post.dict())
        return dict(code=200, msg='添加项目成功', data=post)
    return dict(code=403, msg='项目已存在,请更换项目名')


@tester.put('/project', summary='更新项目', response=Message)
def update_project(request, pid: int, put: ProjectBase):
    try:
        project = ProjectCRUD.get_project_by_id(pid)
    except Http404:
        return dict(code=404, msg='项目不存在,请重新输入')
    if not ProjectCRUD.get_project_name_by_id(pid) == put.name:
        if ProjectCRUD.get_project_name(put):
            return dict(code=403, msg='项目已存在,请更换项目名')
    for attr, value in put.dict().items():
        setattr(project, attr, value)
    project.save()
    return dict(code=200, msg='更新项目成功', data=put)


@tester.delete('/project', summary='删除项目', response=Message)
def delete_project(request, pid: int):
    try:
        project = ProjectCRUD.get_project_by_id(pid)
    except Http404:
        return dict(code=404, msg='项目不存在,请重新输入')
    project.delete()
    return dict(code=200, msg='删除项目成功', data={'id': pid})
