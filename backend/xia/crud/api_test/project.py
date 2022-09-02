#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models.api_test.project import ApiTestProject
from backend.xia.schemas.api_test.project import CreateApiTestProject, UpdateApiTestProject


class CRUDApiTestProject(CRUDBase[ApiTestProject, CreateApiTestProject, UpdateApiTestProject]):

    def get_all_projects(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    def get_all_enable_projects(self) -> QuerySet:
        return self.model.objects.filter(status=1).all().order_by('-modified_time')

    def get_project_by_id(self, pk: int) -> ApiTestProject:
        return super().get(pk=pk)

    def get_project_by_name(self, name: str) -> ApiTestProject:
        return self.model.objects.filter(name=name).first()

    def get_project_name_by_id(self, pk: int) -> str:
        return super().get(pk=pk).name

    def get_project_or_404(self, pk: int) -> ApiTestProject:
        return super().get_object_or_404(pk=pk)

    def get_project_status(self, pk: int) -> str:
        return super().get(pk=pk).status

    @transaction.atomic
    def create_project(self, project: CreateApiTestProject) -> ApiTestProject:
        return super().create(project)

    @transaction.atomic
    def update_project(self, pk: int, project: UpdateApiTestProject) -> ApiTestProject:
        return super().update_one(pk, project)

    def delete_project(self, pk: int) -> ApiTestProject:
        return super().delete_one(pk)

    def get_project_modules(self, pk: int) -> QuerySet:
        return super().get(pk).api_test_modules.all().order_by('-modified_time')

    def get_project_count(self) -> int:
        return super().get_all().count()


ApiTestProjectDao = CRUDApiTestProject(ApiTestProject)
