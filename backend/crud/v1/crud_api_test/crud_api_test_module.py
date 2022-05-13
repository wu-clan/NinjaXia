#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestModule
from backend.schemas.v1.sm_api_test.sm_api_test_module import CreateApiTestModule, UpdateApiTestModule


class CRUDApiTestTask(CRUDBase[ApiTestModule, CreateApiTestModule, UpdateApiTestModule]):

    def get_all_modules(self) -> QuerySet:
        return super().get_all()

    def get_module_by_name(self, module_name: int) -> str:
        return self.model.objects.filter(name=module_name).first()


crud_api_test_module = CRUDApiTestTask(ApiTestModule)
