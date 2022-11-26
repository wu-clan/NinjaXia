#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.xia.common.exception import errors
from backend.xia.crud.sys.email import SysEmailSenderDao, SysEmailReceiverGroupDao, SysEmailReceiverDao
from backend.xia.schemas.sys.email import UpdateSysEmailSender, CreateSysEmailSender, \
    CreateSysEmailReceiverGroup, UpdateSysEmailReceiverGroup, CreateSysEmailReceiver, UpdateSysEmailReceiver


def get_sender_info():
    sender = SysEmailSenderDao.get_sender()
    if not sender:
        raise errors.NotFoundError(msg='没有发送者信息')
    return sender


def create_sender(*, request, obj: CreateSysEmailSender):
    sender = SysEmailSenderDao.get_sender()
    if sender:
        raise errors.ForbiddenError(msg='发送者已存在')
    new_sender = SysEmailSenderDao.create_sender(obj, request.session['user'])
    return new_sender


def update_sender(*, request, obj: UpdateSysEmailSender):
    sender = SysEmailSenderDao.get_sender()
    if not sender:
        raise errors.NotFoundError(msg='发送者不存在')
    count = SysEmailSenderDao.update_sender(sender.id, obj, request.session['user'])
    return count


def get_all_receiver_groups():
    return SysEmailReceiverGroupDao.get_all_receiver_group()


def get_all_receivers_by_group_id(pk: int):
    group = SysEmailReceiverGroupDao.get_receiver_group_by_id(pk)
    if not group:
        raise errors.NotFoundError(msg='接收者组不存在')
    data = SysEmailReceiverGroupDao.get_all_receiver_by_group_id(pk)
    return data


def create_receiver_group(*, request, obj: CreateSysEmailReceiverGroup):
    group_name = SysEmailReceiverGroupDao.get_receiver_group_by_name(obj.name)
    if group_name:
        raise errors.ForbiddenError(msg='组名已存在, 请更换组名')
    group = SysEmailReceiverGroupDao.create_receiver_group(obj, request.session['user'])
    return group


def update_receiver_group(*, request, pk: int, obj: UpdateSysEmailReceiverGroup):
    group = SysEmailReceiverGroupDao.get_receiver_group_by_id(pk)
    if not group:
        raise errors.NotFoundError(msg='接收者组不存在')
    if group.name != obj.name:
        if SysEmailReceiverGroupDao.get_receiver_group_by_name(obj.name):
            raise errors.ForbiddenError(msg='组名已存在, 请更换组名')
    count = SysEmailReceiverGroupDao.update_receiver_group(pk, obj, request.session['user'])
    return count


def delete_receiver_group(pk: int):
    group = SysEmailReceiverGroupDao.get_receiver_group_by_id(pk)
    if not group:
        raise errors.NotFoundError(msg='接收者组不存在')
    count = SysEmailReceiverGroupDao.delete_receiver_group(pk)
    return count


def get_all_receivers():
    return SysEmailReceiverDao.get_all_receiver()


def create_receiver(*, request, obj: CreateSysEmailReceiver):
    receiver = SysEmailReceiverDao.get_receiver_by_name(obj.name)
    if receiver:
        raise errors.ForbiddenError(msg='接收者已存在, 请更换名称')
    receiver_email = SysEmailReceiverDao.get_receiver_by_email(obj.email)
    if receiver_email:
        raise errors.ForbiddenError(msg='邮箱已存在, 请更换邮箱')
    receiver_group = SysEmailReceiverGroupDao.get_receiver_group_by_id(obj.receiver_group)
    if not receiver_group:
        raise errors.NotFoundError(msg='接收者组不存在')
    obj.receiver_group = receiver_group
    receiver = SysEmailReceiverDao.create_receiver(obj, request.session['user'])
    return receiver


def update_receiver(*, request, pk: int, obj: UpdateSysEmailReceiver):
    receiver = SysEmailReceiverDao.get_receiver_by_id(pk)
    if not receiver:
        raise errors.NotFoundError(msg='接收者不存在')
    if not receiver.name == obj.name:
        receiver_name = SysEmailReceiverDao.get_receiver_by_name(obj.name)
        if receiver_name:
            raise errors.ForbiddenError(msg='接收者已存在, 请更换名称')
    if not receiver.email == obj.email:
        receiver_email = SysEmailReceiverDao.get_receiver_by_email(obj.email)
        if receiver_email:
            raise errors.ForbiddenError(msg='邮箱已存在, 请更换邮箱')
    receiver_group = SysEmailReceiverGroupDao.get_receiver_group_by_id(obj.receiver_group)
    if not receiver_group:
        raise errors.NotFoundError(msg='接收者组不存在')
    obj.receiver_group = receiver_group
    count = SysEmailReceiverDao.update_receiver(pk, obj, request.session['user'])
    return count


def delete_receiver(pk: int):
    receiver = SysEmailReceiverDao.get_receiver_by_id(pk)
    if not receiver:
        raise errors.NotFoundError(msg='接收者不存在')
    count = SysEmailReceiverDao.delete_receiver(pk)
    return count
