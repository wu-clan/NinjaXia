#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import ApiTestEnvironment
from backend.xia.schemas.api_test.env import CreateApiTestEnv
from backend.xia.schemas.api_test.task import UpdateApiTestTask


class CRUDApiTestTask(CRUDBase[ApiTestEnvironment, CreateApiTestEnv, UpdateApiTestTask]):

    def get_all_envs(self) -> QuerySet:
        return super().get_all().order_by('-updated_time')

    def get_all_enable_envs(self) -> QuerySet:
        return self.model.objects.filter(status=True).all().order_by('-updated_time')

    def get_env_by_id(self, pk: int) -> ApiTestEnvironment:
        return super().get(pk)

    def get_env_or_404(self, pk: int) -> ApiTestEnvironment:
        return super().get_object_or_404(pk)

    def get_env_by_name(self, name: str) -> ApiTestEnvironment:
        return self.model.objects.filter(name=name).first()

    @transaction.atomic
    def create_env(self, data: CreateApiTestEnv, user_id: int) -> ApiTestEnvironment:
        return super().create(data, user_id)

    @transaction.atomic
    def update_env(self, pk: int, data: UpdateApiTestTask, user_id: int) -> int:
        return super().update(pk, data, user_id)

    @transaction.atomic
    def delete_env(self, pk: int) -> int:
        return super().delete(pk)

    def get_env_cases(self, pk: int) -> QuerySet:
        return super().get(pk).api_test_cases.all().order_by('-updated_time')

    def get_env_count(self) -> int:
        return super().get_all().count()


ApiTestEnvDao = CRUDApiTestTask(ApiTestEnvironment)
