#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import ApiTestCase
from backend.xia.schemas.api_test.case import CreateApiTestCase, UpdateApiTestCase


class CRUDApiTestTask(CRUDBase[ApiTestCase, CreateApiTestCase, UpdateApiTestCase]):

    def get_all_cases(self) -> QuerySet:
        return super().get_all().order_by('-updated_time')

    def get_cases_by_method(self, method: str) -> QuerySet:
        return self.model.objects.filter(method=method).all().order_by('-updated_time')

    def get_one_case(self, pk: int) -> ApiTestCase:
        return self.model.objects.prefetch_related('api_module', 'api_environment').filter(id=pk).first()

    def get_case_by_id(self, pk: int) -> ApiTestCase:
        return super().get(pk)

    def get_case_by_name(self, name: str) -> ApiTestCase:
        return self.model.objects.filter(name=name).first()

    @transaction.atomic
    def create_case(self, data: CreateApiTestCase, user_id: int) -> ApiTestCase:
        case = super().create(data, user_id)
        return case

    @transaction.atomic
    def update_case(self, pk: int, data: UpdateApiTestCase, user_id: int) -> int:
        return super().update(pk, data, user_id)

    @transaction.atomic
    def delete_cases(self, pk: list) -> tuple:
        return self.model.objects.filter(id__in=pk).delete()[0]

    def get_case_count(self) -> int:
        return super().get_all().count()


ApiTestCaseDao = CRUDApiTestTask(ApiTestCase)
