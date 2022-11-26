#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.sys import email_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.sys.email import GetAllSysEmailReceiverGroup, CreateSysEmailReceiverGroup, \
    UpdateSysEmailReceiverGroup, GetAllSysEmailReceiver, CreateSysEmailReceiver, UpdateSysEmailReceiver, \
    CreateSysEmailSender, UpdateSysEmailSender

v1_sys_email = Router()


@v1_sys_email.get("/senders", summary='获取系统邮件发送者信息', auth=GetCurrentUser())
def get_sys_email_sender(request):
    sender = email_service.get_sender_info()
    return response_base.response_200(data=sender, is_queryset=True, exclude={'_state'})


@v1_sys_email.post('/senders', summary='创建系统邮件发送者信息', auth=GetCurrentIsSuperuser())
def create_sys_email_sender(request, obj: CreateSysEmailSender):
    email_service.create_sender(request=request, obj=obj)
    return response_base.response_200()


@v1_sys_email.put("/senders", summary='更新系统邮件发送者信息', auth=GetCurrentIsSuperuser())
def update_sys_email_sender(request, obj: UpdateSysEmailSender):
    count = email_service.update_sender(request=request, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_email.get("/receiver_groups", summary='获取所有系统邮件接收者组信息', auth=GetCurrentUser(),
                  response=List[GetAllSysEmailReceiverGroup])
@paginate(CustomPagination)
def get_sys_email_receiver_group(request):
    return email_service.get_all_receiver_groups()


@v1_sys_email.get("/receiver_groups/{pk}/receivers", summary='获取指定接收者组下的所有接收者信息',
                  response=List[GetAllSysEmailReceiver], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_sys_email_receiver_by_group_id(request, pk: int):
    return email_service.get_all_receivers_by_group_id(pk)


@v1_sys_email.post("/receiver_groups", summary='创建系统邮件接收者组信息', auth=GetCurrentIsSuperuser())
def create_sys_email_receiver_group(request, obj: CreateSysEmailReceiverGroup):
    email_service.create_receiver_group(request=request, obj=obj)
    return response_base.response_200()


@v1_sys_email.put("/receiver_groups/{pk}", summary='更新系统邮件接收者组信息', auth=GetCurrentIsSuperuser())
def update_sys_email_receiver_group(request, pk: int, obj: UpdateSysEmailReceiverGroup):
    count = email_service.update_receiver_group(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_email.delete("/receiver_groups/{pk}", summary='删除系统邮件接收者组信息', auth=GetCurrentIsSuperuser())
def delete_sys_email_receiver_group(request, pk: int):
    count = email_service.delete_receiver_group(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_email.get("/receivers", summary='获取所有系统邮件接收者信息', response=List[GetAllSysEmailReceiver],
                  auth=GetCurrentUser())
@paginate(CustomPagination)
def get_sys_email_receiver(request):
    return email_service.get_all_receivers()


@v1_sys_email.post("/receivers", summary='创建系统邮件接收者信息', auth=GetCurrentIsSuperuser())
def create_sys_email_receiver(request, obj: CreateSysEmailReceiver):
    email_service.create_receiver(request=request, obj=obj)
    return response_base.response_200()


@v1_sys_email.put("/receivers/{pk}", summary='更新系统邮件接收者信息', auth=GetCurrentIsSuperuser())
def update_sys_email_receiver(request, pk: int, obj: UpdateSysEmailReceiver):
    count = email_service.update_receiver(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_email.delete("/receivers/{pk}", summary='删除系统邮件接收者信息', auth=GetCurrentIsSuperuser())
def delete_sys_email_receiver(request, pk: int):
    count = email_service.delete_receiver(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()
