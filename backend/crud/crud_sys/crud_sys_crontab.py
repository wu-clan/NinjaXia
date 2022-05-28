#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import Crontab
from backend.schemas.sm_sys.sm_sys_crontab import CreateCornTab, UpdateCornTab


class CRUDCrontab(CRUDBase[Crontab, CreateCornTab, UpdateCornTab]):

    def get_all_crontab(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    def get_crontab_by_id(self, pk: int) -> Crontab:
        return super().get(pk)

    @transaction.atomic
    def create_crontab(self, obj: CreateCornTab) -> Crontab:
        return super().create(obj)

    @transaction.atomic
    def update_crontab(self, pk: int, obj: UpdateCornTab) -> Crontab:
        return super().update_one(pk, obj)

    @transaction.atomic
    def delete_crontab(self, pk: int) -> Crontab:
        return super().delete_one(pk)


crud_crontab = CRUDCrontab(Crontab)