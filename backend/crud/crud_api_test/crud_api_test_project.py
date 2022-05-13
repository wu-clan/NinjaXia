#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.ninja_models.models import ApiTestProject
from backend.schemas.sm_api_test.sm_api_test_project import CreateProject, UpdateProject
from backend.crud.base import CRUDBase


class CRUDProject(CRUDBase[ApiTestProject, CreateProject, UpdateProject]):

    def get_all_projects(self) -> ApiTestProject:
        return super().get_all()

    def get_project_by_name(self, name: str) -> ApiTestProject:
        return self.model.objects.filter(name=name).first()

    def get_project_name_by_id(self, pk: int) -> str:
        return super().get(pk=pk).name

    def get_project_by_id(self, pk: int) -> ApiTestProject:
        return super().get_object_or_404(pk=pk)

    def get_project_status(self, pk: int) -> str:
        return super().get(pk=pk).status

    def create_project(self, project: CreateProject) -> ApiTestProject:
        return super().create(project)

    def update_project(self, pk: int, project: UpdateProject) -> ApiTestProject:
        return super().update_one(pk, project)

    def delete_project(self, pk: int) -> ApiTestProject:
        return super().delete_one(pk)


crud_project = CRUDProject(ApiTestProject)
