#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models import ApiTestModule
from backend.xia.schemas.api_test.module import CreateApiTestModule, UpdateApiTestModule


class CRUDApiTestTask(CRUDBase[ApiTestModule, CreateApiTestModule, UpdateApiTestModule]):

    def get_all_modules(self) -> QuerySet:
        return super().get_all().order_by('-updated_time')

    def get_one_module(self, pk: int) -> QuerySet:
        return self.model.objects.select_related('api_project').filter(id=pk).first()

    def get_module_by_id(self, pk: int) -> ApiTestModule:
        return super().get(pk=pk)

    def get_module_or_404(self, pk: int) -> ApiTestModule:
        return super().get_object_or_404(pk)

    def get_module_by_name(self, module_name: int) -> str:
        return self.model.objects.filter(name=module_name).first()

    def get_module_name_by_id(self, pk: int) -> str:
        return self.get(pk=pk).name

    @transaction.atomic
    def create_module(self, create_module: CreateApiTestModule, user_id: int) -> ApiTestModule:
        return super().create(create_module, user_id)

    @transaction.atomic
    def update_module(self, pk: int, update_module: UpdateApiTestModule, user_id: int) -> int:
        return super().update(pk, update_module, user_id)

    @transaction.atomic
    def delete_module(self, pk: int) -> int:
        return super().delete(pk)

    def get_module_cases(self, pk: int) -> QuerySet:
        return super().get(pk=pk).api_test_cases.all().order_by('-updated_time')

    def get_module_count(self) -> int:
        return super().get_all().count()


ApiTestModuleDao = CRUDApiTestTask(ApiTestModule)
