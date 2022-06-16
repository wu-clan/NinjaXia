#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import SysEmailSender, SysEmailReceiverGroup, SysEmailReceiver
from backend.schemas.sm_sys.sm_sys_email import CreateSysEmailSender, UpdateSysEmailSender, \
    CreateSysEmailReceiverGroup, UpdateSysEmailReceiverGroup, CreateSysEmailReceiver, UpdateSysEmailReceiver


class CRUDSender(CRUDBase[SysEmailSender, CreateSysEmailSender, UpdateSysEmailSender]):

    def get_sender(self) -> QuerySet:
        return super().get_all()

    def create_sender(self, obj: CreateSysEmailSender) -> SysEmailSender:
        return super().create(obj)

    def update_sender(self, pk: int, obj: UpdateSysEmailSender) -> SysEmailSender:
        return super().update_one(pk, obj)

    def get_smtp_server(self) -> SysEmailSender:
        return super().get_all()[0].smtp_server

    def get_smtp_port(self) -> SysEmailSender:
        return super().get_all()[0].smtp_port

    def get_sender_name(self) -> str:
        return super().get_all()[0].name

    def get_sender_email(self) -> str:
        return super().get_all()[0].email

    def get_sender_password(self) -> str:
        return super().get_all()[0].password

    def get_is_ssl(self) -> bool:
        return super().get_all()[0].is_ssl


SysEmailSenderDao = CRUDSender(SysEmailSender)


class CRUDReceiverGroup(CRUDBase[SysEmailReceiverGroup, CreateSysEmailReceiverGroup, UpdateSysEmailReceiverGroup]):

    def get_all_receiver_group(self) -> QuerySet:
        return super().get_all()

    def get_all_receiver_by_group_id(self, pk: int) -> QuerySet:
        return self.model.objects.filter(receiver__receiver_group=pk).all()

    def get_receiver_group_by_name(self, name: str) -> SysEmailReceiverGroup:
        return self.model.objects.filter(name=name).first()

    def create_receiver_group(self, obj: CreateSysEmailReceiverGroup) -> SysEmailReceiverGroup:
        return super().create(obj)

    def get_receiver_group_by_id(self, pk: int) -> SysEmailReceiverGroup:
        return super().get(pk)

    def update_receiver_group(self, pk: int, obj: UpdateSysEmailReceiverGroup) -> SysEmailReceiverGroup:
        return super().update_one(pk, obj)

    def delete_receiver_group(self, pk: int) -> SysEmailReceiverGroup:
        return super().delete_one(pk)


SysEmailReceiverGroupDao = CRUDReceiverGroup(SysEmailReceiverGroup)


class CRUDReceiver(CRUDBase[SysEmailReceiver, CreateSysEmailReceiver, UpdateSysEmailReceiver]):

    def get_all_receiver(self) -> QuerySet:
        return super().get_all()

    def get_receiver_by_name(self, name: str) -> SysEmailReceiver:
        return self.model.objects.filter(name=name).first()

    def get_receiver_by_email(self, email: str) -> SysEmailReceiver:
        return self.model.objects.filter(email=email).first()

    def create_receiver(self, obj: CreateSysEmailReceiver) -> SysEmailReceiver:
        return super().create(obj)

    def get_receiver_by_id(self, pk: int) -> SysEmailReceiver:
        return super().get(pk)

    def update_receiver(self, pk: int, obj: UpdateSysEmailReceiver) -> SysEmailReceiver:
        return super().update_one(pk, obj)

    def delete_receiver(self, pk: int) -> SysEmailReceiver:
        return super().delete_one(pk)


SysEmailReceiverDao = CRUDReceiver(SysEmailReceiver)
