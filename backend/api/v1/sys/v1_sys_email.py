#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.crud.crud_sys.crud_sys_email import crud_sender, crud_receiver_group, crud_receiver
from backend.schemas import Response200, Response403, Response404
from backend.schemas.sm_sys.sm_sys_email import GetAllSysEmailReceiverGroup, CreateSysEmailReceiverGroup, \
    UpdateSysEmailReceiverGroup, GetAllSysEmailReceiver, CreateSysEmailReceiver, UpdateSysEmailReceiver, \
    SysEmailSenderBase
from backend.utils.serialize_data import serialize_data

v1_sys_email = Router()


@v1_sys_email.get("/senders", summary='获取系统邮件发送者信息', auth=GetCurrentUser())
def get_sys_email_sender(request):
    sender = crud_sender.get_sender()
    return Response200(data=serialize_data(sender))


@v1_sys_email.post("/senders", summary='创建/更新系统邮件发送者信息', auth=GetCurrentIsSuperuser())
def operate_sys_email_sender(request, obj: SysEmailSenderBase):
    is_have = crud_sender.get_sender()
    if is_have:
        sender = crud_sender.update_sender(is_have[0].id, obj)
        return Response200(data=serialize_data(sender))
    sender = crud_sender.create_sender(obj)
    return Response200(data=serialize_data(sender))


@v1_sys_email.get("/receiver_groups", summary='获取所有系统邮件接收者组信息', response=List[GetAllSysEmailReceiverGroup],
                  auth=GetCurrentUser())
@paginate(CustomPagination)
def get_sys_email_receiver_group(request):
    return crud_receiver_group.get_all_receiver_group()


@v1_sys_email.get("/receiver_groups/{pk}/receivers", summary='获取指定接收者组下的所有接收者信息', auth=GetCurrentUser())
def get_sys_email_receiver_by_group_id(request, pk: int):
    group = crud_receiver_group.get_receiver_group_by_id(pk)
    if not group:
        return Response404(msg='接收者组不存在')
    data = crud_receiver_group.get_all_receiver_by_group_id(pk)
    return Response200(data=serialize_data(data))


@v1_sys_email.post("/receiver_groups", summary='创建系统邮件接收者组信息', auth=GetCurrentIsSuperuser())
def create_sys_email_receiver_group(request, obj: CreateSysEmailReceiverGroup):
    group_name = crud_receiver_group.get_receiver_group_by_name(obj.name)
    if group_name:
        return Response403(msg='该组名已存在, 请更换组名')
    _group = crud_receiver_group.create_receiver_group(obj)
    return Response200(data=serialize_data(_group))


@v1_sys_email.put("/receiver_groups/{pk}", summary='更新系统邮件接收者组信息', auth=GetCurrentIsSuperuser())
def update_sys_email_receiver_group(request, pk: int, obj: UpdateSysEmailReceiverGroup):
    group = crud_receiver_group.get_receiver_group_by_id(pk)
    if not group:
        return Response404(msg='该组不存在')
    if not group.name == obj.name:
        group_name = crud_receiver_group.get_receiver_group_by_name(obj.name)
        if group_name:
            return Response403(msg='该组名已存在, 请更换组名')
    _group = crud_receiver_group.update_receiver_group(pk, obj)
    return Response200(data=serialize_data(_group))


@v1_sys_email.delete("/receiver_groups/{pk}", summary='删除系统邮件接收者组信息', auth=GetCurrentIsSuperuser())
def delete_sys_email_receiver_group(request, pk: int):
    group = crud_receiver_group.get_receiver_group_by_id(pk)
    if not group:
        return Response404(msg='该组不存在')
    _group = crud_receiver_group.delete_receiver_group(pk)
    return Response200(data=serialize_data(_group))


@v1_sys_email.get("/receivers", summary='获取所有系统邮件接收者信息', response=List[GetAllSysEmailReceiver], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_sys_email_receiver(request):
    return crud_receiver.get_all_receiver()


@v1_sys_email.post("/receivers", summary='创建系统邮件接收者信息', auth=GetCurrentIsSuperuser())
def create_sys_email_receiver(request, obj: CreateSysEmailReceiver):
    receiver = crud_receiver.get_receiver_by_name(obj.name)
    if receiver:
        return Response403(msg='该接收者已存在, 请更换名称')
    receiver_email = crud_receiver.get_receiver_by_email(obj.email)
    if receiver_email:
        return Response403(msg='该邮箱已存在, 请更换邮箱')
    receiver_group = crud_receiver_group.get_receiver_group_by_id(obj.receiver_group)
    if not receiver_group:
        return Response404(msg='该组不存在')
    obj.receiver_group = receiver_group
    _receiver = crud_receiver.create_receiver(obj)
    return Response200(data=serialize_data(_receiver))


@v1_sys_email.put("/receivers/{pk}", summary='更新系统邮件接收者信息', auth=GetCurrentIsSuperuser())
def update_sys_email_receiver(request, pk: int, obj: UpdateSysEmailReceiver):
    receiver = crud_receiver.get_receiver_by_id(pk)
    if not receiver:
        return Response404(msg='该接收者不存在')
    if not receiver.name == obj.name:
        receiver_name = crud_receiver.get_receiver_by_name(obj.name)
        if receiver_name:
            return Response403(msg='该接收者已存在, 请更换名称')
    if not receiver.email == obj.email:
        receiver_email = crud_receiver.get_receiver_by_email(obj.email)
        if receiver_email:
            return Response403(msg='该邮箱已存在, 请更换邮箱')
    receiver_group = crud_receiver_group.get_receiver_group_by_id(obj.receiver_group)
    if not receiver_group:
        return Response404(msg='该组不存在')
    obj.receiver_group = receiver_group
    _receiver = crud_receiver.update_receiver(pk, obj)
    return Response200(data=serialize_data(_receiver))


@v1_sys_email.delete("/receivers/{pk}", summary='删除系统邮件接收者信息', auth=GetCurrentIsSuperuser())
def delete_sys_email_receiver(request, pk: int):
    receiver = crud_receiver.get_receiver_by_id(pk)
    if not receiver:
        return Response404(msg='该接收者不存在')
    _receiver = crud_receiver.delete_receiver(pk)
    return Response200(data=serialize_data(_receiver))
