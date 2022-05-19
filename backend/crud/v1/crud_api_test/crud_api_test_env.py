#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestEnvironment
from backend.schemas.v1.sm_api_test.sm_api_test_env import CreateApiTestEnv
from backend.schemas.v1.sm_api_test.sm_api_test_task import UpdateApiTestTask


class CRUDApiTestTask(CRUDBase[ApiTestEnvironment, CreateApiTestEnv, UpdateApiTestTask]):

    def get_all_envs(self) -> QuerySet:
        return super().get_all()

    def get_env_by_id(self, pk) -> ApiTestEnvironment:
        return super().get(pk)

    def get_env_by_name(self, name) -> ApiTestEnvironment:
        return self.model.objects.filter(name=name).first()

    def create_env(self, data: CreateApiTestEnv) -> ApiTestEnvironment:
        return super().create(data)

    def update_env(self, pk: int, data: UpdateApiTestTask) -> ApiTestEnvironment:
        return super().update_one(pk, data)

    def delete_env(self, pk: int) -> ApiTestEnvironment:
        return super().delete_one(pk)


crud_api_test_env = CRUDApiTestTask(ApiTestEnvironment)
