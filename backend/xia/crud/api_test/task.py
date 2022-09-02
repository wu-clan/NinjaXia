#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models.api_test.task import ApiTestTask
from backend.xia.schemas.api_test.task import CreateApiTestTask, UpdateApiTestTask


class CRUDApiTestTask(CRUDBase[ApiTestTask, CreateApiTestTask, UpdateApiTestTask]):

    def get_all_tasks(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    def get_task_by_name(self, name: str) -> ApiTestTask:
        return self.model.objects.filter(name=name).first()

    def get_task_by_id(self, task_id: int) -> ApiTestTask:
        return super().get(task_id)

    @transaction.atomic
    def create_task(self, create_data: CreateApiTestTask) -> ApiTestTask:
        return self.model.objects.create(**create_data.dict(), state=0)

    @transaction.atomic
    def update_task(self, task_id: int, update_data: UpdateApiTestTask) -> ApiTestTask:
        state = super().get(task_id).state
        task = self.model.objects.filter(id=task_id)
        task.update(**update_data.dict(), state=state)
        return task.first()

    @transaction.atomic
    def delete_task(self, task_id: int) -> ApiTestTask:
        return super().delete_one(task_id)

    def get_task_count(self) -> int:
        return super().get_all().count()


ApiTestTaskDao = CRUDApiTestTask(ApiTestTask)
