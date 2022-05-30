#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import Sender, ReceiverGroup, Receiver
from backend.schemas.sm_sys.sm_sys_email import CreateSysEmailSender, UpdateSysEmailSender, \
    CreateSysEmailReceiverGroup, UpdateSysEmailReceiverGroup, CreateSysEmailReceiver, UpdateSysEmailReceiver


class CRUDSender(CRUDBase[Sender, CreateSysEmailSender, UpdateSysEmailSender]):

    def get_sender(self) -> QuerySet:
        return super().get_all()

    def create_sender(self, obj: CreateSysEmailSender) -> Sender:
        return super().create(obj)

    def update_sender(self, pk: int, obj: UpdateSysEmailSender) -> Sender:
        return super().update_one(pk, obj)

    def get_smtp_server(self) -> Sender:
        return super().get_all()[0].smtp_server

    def get_smtp_port(self) -> Sender:
        return super().get_all()[0].smtp_port

    def get_sender_name(self) -> str:
        return super().get_all()[0].name

    def get_sender_email(self) -> str:
        return super().get_all()[0].email

    def get_sender_password(self) -> str:
        return super().get_all()[0].password

    def get_is_ssl(self) -> bool:
        return super().get_all()[0].is_ssl


crud_sender = CRUDSender(Sender)


class CRUDReceiverGroup(CRUDBase[ReceiverGroup, CreateSysEmailReceiverGroup, UpdateSysEmailReceiverGroup]):

    def get_all_receiver_group(self) -> QuerySet:
        return super().get_all()

    def get_all_receiver_by_group_id(self, pk: int) -> QuerySet:
        return self.model.objects.filter(receiver__receiver_group=pk).all()

    def get_receiver_group_by_name(self, name: str) -> ReceiverGroup:
        return self.model.objects.filter(name=name).first()

    def create_receiver_group(self, obj: CreateSysEmailReceiverGroup) -> ReceiverGroup:
        return super().create(obj)

    def get_receiver_group_by_id(self, pk: int) -> ReceiverGroup:
        return super().get(pk)

    def update_receiver_group(self, pk: int, obj: UpdateSysEmailReceiverGroup) -> ReceiverGroup:
        return super().update_one(pk, obj)

    def delete_receiver_group(self, pk: int) -> ReceiverGroup:
        return super().delete_one(pk)


crud_receiver_group = CRUDReceiverGroup(ReceiverGroup)


class CRUDReceiver(CRUDBase[Receiver, CreateSysEmailReceiver, UpdateSysEmailReceiver]):

    def get_all_receiver(self) -> QuerySet:
        return super().get_all()

    def get_receiver_by_name(self, name: str) -> Receiver:
        return self.model.objects.filter(name=name).first()

    def get_receiver_by_email(self, email: str) -> Receiver:
        return self.model.objects.filter(email=email).first()

    def create_receiver(self, obj: CreateSysEmailReceiver) -> Receiver:
        return super().create(obj)

    def get_receiver_by_id(self, pk: int) -> Receiver:
        return super().get(pk)

    def update_receiver(self, pk: int, obj: UpdateSysEmailReceiver) -> Receiver:
        return super().update_one(pk, obj)

    def delete_receiver(self, pk: int) -> Receiver:
        return super().delete_one(pk)


crud_receiver = CRUDReceiver(Receiver)
