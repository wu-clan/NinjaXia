#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from django.http import Http404
from ninja import Router

from backend.common.log import log
from backend.ninja_models.models.api_auto.interface import InterfaceCRUD
from backend.schemas import Message
from backend.schemas.interface import InterfaceBase, GetInterface

interface = Router()


@interface.post('/interface', summary='添加接口组', response=Message)
def add_project(request, post: InterfaceBase, p_name: str, ):
    if not InterfaceCRUD.get_interface_name_by_name(post.name):
        try:
            pid = InterfaceCRUD.get_project_id_by_name(p_name)
        except AttributeError:
            return dict(code=403, msg='项目不存在，请先添加项目')
        InterfaceCRUD.create_interface(post, pid)
        log.success(f'添加接口组 {post.name} 成功')
        return dict(code=200, msg='添加接口组成功', data=post)
    return dict(code=403, msg='接口组已存在，请更换接口组名')


@interface.put('/interface/{iid}', summary='更新接口组', response=Message)
def update_project(request, iid: int, put: InterfaceBase):
    try:
        api = InterfaceCRUD.get_interface(iid)
    except Http404:
        log.error('输入有误，要更新的接口组不存在')
        return dict(code=404, msg='接口组不存在，请重新输入')
    _name = InterfaceCRUD.get_interface_name_by_id(iid)
    if not _name == put.name:
        if InterfaceCRUD.get_interface_name_by_name(put.name):
            log.error(f'更新项目名 {_name} 为 {put.name} 失败， {put.name} 项目已存在')
            return dict(code=403, msg='项目已存在，请更换项目名')
    for attr, value in put.dict().items():
        setattr(api, attr, value)
    api.save()
    log.success(f'接口组 {_name} 更新成功')
    return dict(code=200, msg='接口组更新成功', data=put)


@interface.delete('/interface/{iid}', summary='删除接口组', response=Message)
def delete_project(request, iid: int):
    try:
        api = InterfaceCRUD.get_interface(iid)
        _name = InterfaceCRUD.get_interface_name_by_id(iid)
    except Http404:
        log.error(f'接口组不存在，请重新输入')
        return dict(code=404, msg='接口组不存在，请重新输入')
    api.delete()
    log.success(f'删除接口组 {_name} 成功')
    return dict(code=200, msg='删除接口组成功')


@interface.get('/interface', summary='获取所有接口组', response=List[GetInterface])
def get_project(request):
    _interfaces = InterfaceCRUD.get_all_interfaces()
    log.success('获取所有接口组成功')
    return _interfaces
