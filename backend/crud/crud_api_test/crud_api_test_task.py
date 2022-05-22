#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models.api_test.api_test_task import ApiTestTask
from backend.schemas.sm_api_test.sm_api_test_task import CreateApiTestTask, UpdateApiTestTask


class CRUDApiTestTask(CRUDBase[ApiTestTask, CreateApiTestTask, UpdateApiTestTask]):

    def get_all_tasks(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')


crud_api_test_task = CRUDApiTestTask(ApiTestTask)
