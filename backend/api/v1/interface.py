#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.common.log import log
from backend.ninja_models.models.api_auto.interface import InterfaceCRUD
from backend.schemas import Message
from backend.schemas.interface import InterfaceBase, GetInterface, CreateInterface, UpdateInterface

interface = Router()


@interface.post('/interface', summary='添加接口组', response=Message)
def add_interface(request, post: InterfaceBase, project: CreateInterface):
    if not InterfaceCRUD.get_interface_by_name(post.name):
        try:
            InterfaceCRUD.get_project_for_interface(project.id)
        except Http404:
            log.error(f'project {project.id} does not exist，please add items first')
            return dict(code=403, msg='项目不存在，请先添加项目')
        InterfaceCRUD.create_interface(post, project.id)
        log.success(f'add interface group {post.name} success')
        return dict(code=200, msg='添加接口组成功', data=post)
    log.error(f'add interface group {post.name} fail，interface group already exists，please change the interface group name')
    return dict(code=403, msg='添加接口组失败，接口组已存在，请更换接口组名')


@interface.put('/interface/{iid}', summary='更新接口组', response=Message)
def update_interface(request, iid: int, put: InterfaceBase, pid: UpdateInterface):
    try:
        api = InterfaceCRUD.get_interface(iid)
    except Http404:
        log.error('input error，the interface group to be updated does not exist')
        return dict(code=404, msg='接口组不存在，请重新输入')
    _name = InterfaceCRUD.get_interface_name_by_id(iid)
    if not _name == put.name:
        if InterfaceCRUD.get_interface_by_name(put.name):
            log.error(f'update interface group name {_name} to {put.name} fail， {put.name} interface group already exists')
            return dict(code=403, msg='接口组已存在，请更换接口组名')
    try:
        InterfaceCRUD.get_project_for_interface(pid.id)
    except Http404:
        log.error(f'project {pid.id} does not exist，please add items first')
        return dict(code=404, msg='项目不存在，请先添加项目')
    for attr, value in put.dict().items():
        setattr(api, attr, value)
    api.project_id = pid.id
    api.save()
    log.success(f'interface group {_name} update completed')
    return dict(code=200, msg='接口组更新成功', data=put)


@interface.delete('/interface/{iid}', summary='删除接口组', response=Message)
def delete_interface(request, iid: int):
    try:
        api = InterfaceCRUD.get_interface(iid)
        _name = InterfaceCRUD.get_interface_name_by_id(iid)
    except Http404:
        log.error('interface group does not exist，please enter again')
        return dict(code=404, msg='接口组不存在，请重新输入')
    api.delete()
    log.success(f'delete interface group {_name} success')
    return dict(code=200, msg='删除接口组成功')


@interface.get('/interface', summary='获取所有接口组', response=List[GetInterface])
@paginate
def get_interface(request, **kwargs):
    _interfaces = InterfaceCRUD.get_all_interfaces()
    log.success('get all interface groups successfully')
    return _interfaces
