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


crud_api_test_env = CRUDApiTestTask(ApiTestEnvironment)
