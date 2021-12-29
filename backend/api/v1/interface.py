#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from ninja import Router

from backend.common.log import log
from backend.ninja_models.models.api_auto.interface import InterfaceCRUD
from backend.schemas import Message
from backend.schemas.interface import InterfaceBase, GetInterface, CreateInterface

interface = Router()


@interface.post('/interface', summary='添加接口组', response=Message)
def add_project(request, p_name: CreateInterface, post: InterfaceBase):
    if not InterfaceCRUD.get_interface_name(post.name):
        if p_name is not None:
            pid = InterfaceCRUD.get_project_id_by_name(p_name)
            InterfaceCRUD.create_interface(post, pid)
            log.success(f'添加接口组 {post.name} 成功')
            return dict(code=200, msg='添加接口组成功', data=post)
        return dict(code=403, msg='接口组已存在,请更换接口组名')


@interface.put('/interface', summary='更新接口组', response=Message)
def update_project(request, pid: int, put: InterfaceBase):
    pass


@interface.delete('/interface', summary='删除接口组', response=Message)
def delete_project(request, pid: int):
    pass


@interface.get('/interface', summary='获取所有接口组', response=List[GetInterface])
def get_project(request):
    _interfaces = InterfaceCRUD.get_all_interfaces()
    log.success('获取所有接口组成功')
    return _interfaces
