#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.ninja_models.models import ApiProject
from backend.schemas.sm_project import CreateProject, UpdateProject
from backend.crud.base import CRUDBase


class CRUDProject(CRUDBase[ApiProject, CreateProject, UpdateProject]):

    def get_all_projects(self) -> ApiProject:
        return super().get_all()

    def get_project_by_name(self, name: str) -> ApiProject:
        return self.model.objects.filter(name=name).first()

    def get_project_name_by_id(self, pk: int) -> str:
        return super().get(pk=pk).name

    def get_project_by_id(self, pk: int) -> ApiProject:
        return super().get_object_or_404(pk=pk)

    def get_project_status(self, pk: int) -> str:
        return super().get(pk=pk).status

    def create_project(self, project: CreateProject) -> ApiProject:
        return super().create(project)

    def update_project(self, pk: int, project: UpdateProject) -> ApiProject:
        return super().update_one(pk, project)

    def delete_project(self, pk: int) -> ApiProject:
        return super().delete_one(pk)


crud_project = CRUDProject(ApiProject)
