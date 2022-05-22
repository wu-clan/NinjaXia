#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestBusinessTest
from backend.schemas.sm_api_test.sm_api_test_business import CreateApiTestBusiness, UpdateApiTestBusiness


class CRUDApiTestTask(CRUDBase[ApiTestBusinessTest, CreateApiTestBusiness, UpdateApiTestBusiness]):

    def get_all_businesses(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')


crud_api_test_business = CRUDApiTestTask(ApiTestBusinessTest)
