#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestCase
from backend.schemas.sm_api_test.sm_api_test_case import CreateApiTestCase, UpdateApiTestCase


class CRUDApiTestTask(CRUDBase[ApiTestCase, CreateApiTestCase, UpdateApiTestCase]):

    def get_all_cases(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    def get_case_by_id(self, pk: int) -> ApiTestCase:
        return super().get(pk)

    def get_case_by_name(self, name: str) -> ApiTestCase:
        return self.model.objects.filter(name=name).first()

    @transaction.atomic
    def create_case(self, data: CreateApiTestCase) -> ApiTestCase:
        case = super().create(data)
        case.params = json.loads(str(case.params))
        case.headers = json.loads(str(case.headers))
        return case

    @transaction.atomic
    def update_case(self, pk: int, data: UpdateApiTestCase) -> ApiTestCase:
        case = super().update_one(pk, data)
        case.params = json.loads(str(case.params))
        case.headers = json.loads(str(case.headers))
        return case

    def delete_case(self, pk: list) -> tuple:
        return self.model.objects.filter(id__in=pk).delete()


crud_api_test_case = CRUDApiTestTask(ApiTestCase)
