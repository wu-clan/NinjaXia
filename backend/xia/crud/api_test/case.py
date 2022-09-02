#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import ApiTestCase
from backend.xia.schemas.api_test.case import CreateApiTestCase, UpdateApiTestCase


class CRUDApiTestTask(CRUDBase[ApiTestCase, CreateApiTestCase, UpdateApiTestCase]):

    def get_all_cases(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    def get_one_case(self, pk: int) -> ApiTestCase:
        return self.model.objects.select_related('api_module', 'api_environment').filter(id=pk).first()

    def get_case_by_id(self, pk: int) -> ApiTestCase:
        return super().get(pk)

    def get_case_by_name(self, name: str) -> ApiTestCase:
        return self.model.objects.filter(name=name).first()

    @transaction.atomic
    def create_case(self, data: CreateApiTestCase) -> ApiTestCase:
        case = super().create(data)
        case.params = json.loads(str(case.params))
        case.headers = json.loads(str(case.headers))
        if data.body_type == 'JSON' or data.body_type == 'form-data' or data.body_type == 'x-www-form-urlencoded' or \
                data.body_type == 'binary' or data.body_type == 'GraphQL':
            case.body = json.loads(str(case.body))
        return case

    @transaction.atomic
    def update_case(self, pk: int, data: UpdateApiTestCase) -> ApiTestCase:
        case = super().update_one(pk, data)
        case.params = json.loads(str(case.params))
        case.headers = json.loads(str(case.headers))
        if data.body_type == 'JSON' or data.body_type == 'form-data' or data.body_type == 'x-www-form-urlencoded' or \
                data.body_type == 'binary' or data.body_type == 'GraphQL':
            case.body = json.loads(str(case.body))
        return case

    def delete_case(self, pk: list) -> tuple:
        return self.model.objects.filter(id__in=pk).delete()

    def get_case_count(self) -> int:
        return super().get_all().count()


ApiTestCaseDao = CRUDApiTestTask(ApiTestCase)
