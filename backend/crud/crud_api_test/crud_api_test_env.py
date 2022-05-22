#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestEnvironment
from backend.schemas.sm_api_test.sm_api_test_env import CreateApiTestEnv
from backend.schemas.sm_api_test.sm_api_test_task import UpdateApiTestTask


class CRUDApiTestTask(CRUDBase[ApiTestEnvironment, CreateApiTestEnv, UpdateApiTestTask]):

    def get_all_envs(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    def get_all_enable_envs(self) -> QuerySet:
        return self.model.objects.filter(status=True).all().order_by('-modified_time')

    def get_env_by_id(self, pk: int) -> ApiTestEnvironment:
        return super().get(pk)

    def get_env_by_name(self, name: str) -> ApiTestEnvironment:
        return self.model.objects.filter(name=name).first()

    def create_env(self, data: CreateApiTestEnv) -> ApiTestEnvironment:
        return super().create(data)

    def update_env(self, pk: int, data: UpdateApiTestTask) -> ApiTestEnvironment:
        return super().update_one(pk, data)

    def delete_env(self, pk: int) -> ApiTestEnvironment:
        return super().delete_one(pk)

    def get_env_cases(self, pk: int) -> QuerySet:
        return self.model.objects.filter(api_test_case__api_environment=pk).all().order_by('-modified_time')


crud_api_test_env = CRUDApiTestTask(ApiTestEnvironment)
