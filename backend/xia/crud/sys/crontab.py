#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import SysCrontab
from backend.xia.schemas.sys.crontab import CreateCornTab, UpdateCornTab


class CRUDSysCrontab(CRUDBase[SysCrontab, CreateCornTab, UpdateCornTab]):

    def get_all_crontab(self) -> QuerySet:
        return super().get_all().order_by('-updated_time')

    def get_crontab_by_id(self, pk: int) -> SysCrontab:
        return super().get(pk)

    @transaction.atomic
    def create_crontab(self, obj: CreateCornTab, user_id: int) -> SysCrontab:
        return super().create(obj, user_id=user_id)

    @transaction.atomic
    def update_crontab(self, pk: int, obj: UpdateCornTab, user_id: int) -> int:
        return super().update(pk, obj, user_id)

    @transaction.atomic
    def delete_crontab(self, pk: int) -> int:
        return super().delete(pk)

    def format_crontab(self, pk: int) -> str:
        corn = super().get(pk)
        return '{c0} {c1} {c2} {c3} {c4} {c5}'.format(
            c0=corn.second, c1=corn.minute, c2=corn.hour, c3=corn.day, c4=corn.month, c5=corn.day_of_week
        )


SysCrontabDao = CRUDSysCrontab(SysCrontab)
