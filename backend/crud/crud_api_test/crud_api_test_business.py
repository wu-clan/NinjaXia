#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.db import transaction
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestBusinessTest, ApiTestBusinessTestAndCase
from backend.schemas.sm_api_test.sm_api_test_business import CreateApiTestBusiness, UpdateApiTestBusiness


class CRUDApiTestTask(CRUDBase[ApiTestBusinessTest, CreateApiTestBusiness, UpdateApiTestBusiness]):

    @staticmethod
    def get_all_businesses() -> QuerySet:
        return ApiTestBusinessTestAndCase.objects.all().order_by('-modified_time')

    @staticmethod
    def get_one_business(pk: int) -> QuerySet:
        return ApiTestBusinessTestAndCase.objects.filter(api_business_test_id=pk).all().order_by(
            '-modified_time').select_related('api_business_test', 'api_case')

    @staticmethod
    def get_all_businesses_by_name(name: str) -> QuerySet:
        return ApiTestBusinessTestAndCase.objects.filter(api_business_test__name__icontains=name).all().order_by(
            '-modified_time').select_related('api_business_test', 'api_case')

    def get_business_by_name(self, name: str) -> ApiTestBusinessTest:
        return self.model.objects.filter(name=name).first()

    def get_business_by_id(self, pk: int) -> ApiTestBusinessTest:
        return super().get(pk)

    @transaction.atomic
    def create_business(self, obj: CreateApiTestBusiness, cases: list) -> [
        ApiTestBusinessTest, List[ApiTestBusinessTestAndCase]
    ]:
        business = self.model.objects.create(**obj.dict(exclude={'api_cases'}))
        business_and_cases = []
        for case in cases:
            business_and_case = ApiTestBusinessTestAndCase.objects.create(api_business_test=business, api_case=case)
            business_and_cases.append(business_and_case)
        return business, business_and_cases

    @transaction.atomic
    def update_business(self, pk: int, obj: UpdateApiTestBusiness, cases: list) -> [
        ApiTestBusinessTest, List[ApiTestBusinessTestAndCase]
    ]:
        business = super().update_one(pk, obj.dict(exclude={'api_cases'}))
        business_and_cases = []
        ApiTestBusinessTestAndCase.objects.filter(api_business_test=pk).delete()
        for case in cases:
            business_and_case = ApiTestBusinessTestAndCase.objects.create(api_business_test=business, api_case=case)
            business_and_cases.append(business_and_case)
        return business, business_and_cases

    @transaction.atomic
    def delete_business(self, pk: int) -> ApiTestBusinessTest:
        business = super().delete_one(pk)
        ApiTestBusinessTestAndCase.objects.filter(api_business_test=pk).delete()
        return business

    @staticmethod
    def get_business_cases(pk: int) -> list:
        cases = []
        tc = ApiTestBusinessTestAndCase.objects.filter(api_business_test=pk).all()
        for case in tc:
            cases.append(case.api_case)
        return cases

    def get_business_count(self) -> int:
        return super().get_all().count()


ApiTestBusinessDao = CRUDApiTestTask(ApiTestBusinessTest)
