#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import ApiTestBusinessTest, ApiTestBusinessTestAndCase
from backend.xia.schemas.api_test.business import CreateApiTestBusiness, UpdateApiTestBusiness


class CRUDApiTestTask(CRUDBase[ApiTestBusinessTest, CreateApiTestBusiness, UpdateApiTestBusiness]):

    def get_all_businesses(self) -> QuerySet:
        return self.model.objects.all().order_by('-updated_time')

    def get_one_business(self, pk: int) -> QuerySet:
        return self.model.objects.select_related('api_module').filter(id=pk).first()

    def get_all_businesses_by_name(self, name: str) -> QuerySet:
        return self.model.objects.filter(name__icontains=name).all().order_by('-updated_time')

    def get_business_by_name(self, name: str) -> ApiTestBusinessTest:
        return self.model.objects.filter(name=name).first()

    def get_business_by_id(self, pk: int) -> ApiTestBusinessTest:
        return super().get(pk)

    @transaction.atomic
    def create_business(self, obj: CreateApiTestBusiness, cases: list, user_id: int) -> [
        ApiTestBusinessTest, List[ApiTestBusinessTestAndCase]
    ]:
        business = self.model.objects.create(**obj.dict(exclude={'api_cases'}), create_user=user_id)
        business_and_cases = []
        for case in cases:
            business_and_cases.append(
                ApiTestBusinessTestAndCase(api_business_test=business, api_case=case, create_user=user_id)
            )
        ApiTestBusinessTestAndCase.objects.bulk_create(business_and_cases)
        return business, business_and_cases

    @transaction.atomic
    def update_business(self, pk: int, obj: UpdateApiTestBusiness, cases: list, user_id: int) -> int:
        count = super().update(pk, obj.dict(exclude={'api_cases'}), user_id)
        ApiTestBusinessTestAndCase.objects.filter(api_business_test=pk).delete()
        business_and_cases = []
        api_business_test = super().get(pk)
        for case in cases:
            business_and_cases.append(
                ApiTestBusinessTestAndCase(
                    api_business_test=api_business_test, api_case=case, create_user=user_id, update_user=user_id
                )
            )
        ApiTestBusinessTestAndCase.objects.bulk_create(business_and_cases)
        return count

    @transaction.atomic
    def delete_business(self, pk: int) -> int:
        count = super().delete(pk)
        return count

    @staticmethod
    def get_business_case_list(pk: int) -> list:
        cases = [ApiTestBusinessTestAndCase.objects.filter(api_business_test=pk).all()]
        return cases

    def get_business_count(self) -> int:
        return super().get_all().count()

    @staticmethod
    def get_all_cases_by_business(pk: int) -> QuerySet:
        return ApiTestBusinessTestAndCase.objects.filter(api_business_test=pk).all().order_by('-updated_time')


ApiTestBusinessDao = CRUDApiTestTask(ApiTestBusinessTest)
