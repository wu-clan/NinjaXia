#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Schema
from pydantic import EmailStr


class SysEmailSenderBase(Schema):
    name: str
    email: EmailStr
    password: str
    smtp_server: str
    smtp_port: int
    is_ssl: bool


class CreateSysEmailSender(SysEmailSenderBase):
    pass


class UpdateSysEmailSender(SysEmailSenderBase):
    pass


class SysEmailReceiverGroupBase(Schema):
    name: str
    description: str


class CreateSysEmailReceiverGroup(SysEmailReceiverGroupBase):
    pass


class UpdateSysEmailReceiverGroup(SysEmailReceiverGroupBase):
    pass


class GetAllSysEmailReceiverGroup(SysEmailReceiverGroupBase):
    id: int


class SysEmailReceiverBase(Schema):
    name: str
    email: EmailStr


class CreateSysEmailReceiver(SysEmailReceiverBase):
    receiver_group: int


class UpdateSysEmailReceiver(SysEmailReceiverBase):
    receiver_group: int


class GetAllSysEmailReceiver(SysEmailReceiverBase):
    id: int
    receiver_group_id: int
