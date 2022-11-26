#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import SysEmailSender, SysEmailReceiverGroup, SysEmailReceiver
from backend.xia.schemas.sys.email import CreateSysEmailSender, UpdateSysEmailSender, \
    CreateSysEmailReceiverGroup, UpdateSysEmailReceiverGroup, CreateSysEmailReceiver, UpdateSysEmailReceiver


class CRUDSender(CRUDBase[SysEmailSender, CreateSysEmailSender, UpdateSysEmailSender]):

    def get_sender(self) -> SysEmailSender:
        return super().get_all().first()

    @transaction.atomic
    def create_sender(self, obj: CreateSysEmailSender, user_id: int) -> SysEmailSender:
        return super().create(obj, user_id)

    @transaction.atomic
    def update_sender(self, pk: int, obj: UpdateSysEmailSender, user_id: int) -> int:
        return super().update(pk, obj, user_id)

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
        group = super().get(pk)
        return group.receivers.all()

    def get_receiver_group_by_name(self, name: str) -> SysEmailReceiverGroup:
        return self.model.objects.filter(name=name).first()

    def get_receiver_group_by_id(self, pk: int) -> SysEmailReceiverGroup:
        return super().get(pk)

    @transaction.atomic
    def create_receiver_group(self, obj: CreateSysEmailReceiverGroup, user_id: int) -> SysEmailReceiverGroup:
        return super().create(obj, user_id)

    @transaction.atomic
    def update_receiver_group(self, pk: int, obj: UpdateSysEmailReceiverGroup, user_id: int) -> int:
        return super().update(pk, obj, user_id)

    @transaction.atomic
    def delete_receiver_group(self, pk: int) -> int:
        return super().delete(pk)


SysEmailReceiverGroupDao = CRUDReceiverGroup(SysEmailReceiverGroup)


class CRUDReceiver(CRUDBase[SysEmailReceiver, CreateSysEmailReceiver, UpdateSysEmailReceiver]):

    def get_all_receiver(self) -> QuerySet:
        return super().get_all()

    def get_receiver_by_name(self, name: str) -> SysEmailReceiver:
        return self.model.objects.filter(name=name).first()

    def get_receiver_by_email(self, email: str) -> SysEmailReceiver:
        return self.model.objects.filter(email=email).first()

    def get_receiver_by_id(self, pk: int) -> SysEmailReceiver:
        return super().get(pk)

    @transaction.atomic
    def create_receiver(self, obj: CreateSysEmailReceiver, user_id: int) -> SysEmailReceiver:
        return super().create(obj, user_id)

    @transaction.atomic
    def update_receiver(self, pk: int, obj: UpdateSysEmailReceiver, user_id: int) -> int:
        return super().update(pk, obj, user_id)

    @transaction.atomic
    def delete_receiver(self, pk: int) -> int:
        return super().delete(pk)


SysEmailReceiverDao = CRUDReceiver(SysEmailReceiver)
