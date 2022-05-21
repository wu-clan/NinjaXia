#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestCase
from backend.schemas.sm_api_test.sm_api_test_case import CreateApiTestCase, UpdateApiTestCase


class CRUDApiTestTask(CRUDBase[ApiTestCase, CreateApiTestCase, UpdateApiTestCase]):

    def get_all_cases(self) -> QuerySet:
        return super().get_all()

    def get_case_by_id(self, pk: int) -> ApiTestCase:
        return super().get(pk)

    def get_case_by_name(self, name: str) -> ApiTestCase:
        return self.model.objects.filter(name=name).first()

    def create_case(self, data: CreateApiTestCase) -> ApiTestCase:
        return super().create(data)

    def update_case(self, pk: int, data: UpdateApiTestCase) -> ApiTestCase:
        return super().update_one(pk, data)

    def delete_case(self, pk: int) -> ApiTestCase:
        return super().delete_one(pk)

    def get_cases_by_env_id(self, pk: int) -> QuerySet:
        return self.model.objects.filter(api_environment=pk)


crud_api_test_case = CRUDApiTestTask(ApiTestCase)
