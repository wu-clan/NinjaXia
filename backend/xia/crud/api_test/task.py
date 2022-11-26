#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models.api_test.task import ApiTestTask
from backend.xia.schemas.api_test.task import CreateApiTestTask, UpdateApiTestTask


class CRUDApiTestTask(CRUDBase[ApiTestTask, CreateApiTestTask, UpdateApiTestTask]):

    def get_all_tasks(self) -> QuerySet:
        return super().get_all().order_by('-updated_time')

    def get_all_tasks_by_project(self, pk: int) -> QuerySet:
        return self.model.objects.filter(api_project=pk).all().order_by('-updated_time')

    def get_task_by_name(self, name: str) -> ApiTestTask:
        return self.model.objects.filter(name=name).first()

    def get_task_by_id(self, task_id: int) -> ApiTestTask:
        return super().get(task_id)

    def get_one_task(self, pk: int):
        return self.model.objects.filter(id=pk).order_by('-updated_time'). \
            select_related('sys_cron', 'api_project', 'api_business_test').first()

    @transaction.atomic
    def create_task(self, create_data: CreateApiTestTask, user_id: int) -> ApiTestTask:
        return super().create(create_data, user_id)

    @transaction.atomic
    def update_task(self, task_id: int, update_data: UpdateApiTestTask, user_id: int) -> int:
        return super().update(task_id, update_data, user_id)

    @transaction.atomic
    def update_task_state(self, task_id: int, state: int, user_id: int) -> int:
        return super().update(task_id, {'state': state}, user_id)

    @transaction.atomic
    def delete_task(self, task_id: int) -> int:
        return super().delete(task_id)

    def get_task_count(self) -> int:
        return super().get_all().count()


ApiTestTaskDao = CRUDApiTestTask(ApiTestTask)
