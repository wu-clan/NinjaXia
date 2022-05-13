#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestCase
from backend.schemas.v1.sm_api_test.sm_api_test_case import CreateApiTestCase, UpdateApiTestCase


class CRUDApiTestTask(CRUDBase[ApiTestCase, CreateApiTestCase, UpdateApiTestCase]):

    def get_all_cases(self) -> QuerySet:
        return super().get_all()


crud_api_test_case = CRUDApiTestTask(ApiTestCase)
