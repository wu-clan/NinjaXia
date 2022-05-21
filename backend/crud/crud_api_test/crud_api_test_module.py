#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models import ApiTestModule
from backend.schemas.sm_api_test.sm_api_test_module import CreateApiTestModule, UpdateApiTestModule


class CRUDApiTestTask(CRUDBase[ApiTestModule, CreateApiTestModule, UpdateApiTestModule]):

    def get_all_modules(self) -> QuerySet:
        return super().get_all()

    def get_module_by_id(self, pk: int) -> ApiTestModule:
        return super().get(pk=pk)

    def get_module_by_name(self, module_name: int) -> str:
        return self.model.objects.filter(name=module_name).first()

    def get_module_name_by_id(self, pk: int) -> str:
        return self.get(pk=pk).name

    def create_module(self, create_module: CreateApiTestModule) -> ApiTestModule:
        return super().create(create_module)

    def update_module(self, pk: int, update_module: UpdateApiTestModule) -> ApiTestModule:
        return super().update_one(pk, update_module)

    def delete_module(self, pk: int) -> ApiTestModule:
        return super().delete_one(pk)

    def get_module_cases(self, pk: int) -> QuerySet:
        return self.model.objects.filter(api_test_case__api_module=pk).all()


crud_api_test_module = CRUDApiTestTask(ApiTestModule)
