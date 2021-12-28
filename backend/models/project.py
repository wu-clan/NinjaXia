# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

from backend.schemas.project import ProjectBase


class Project(models.Model):
    """
    项目管理
    """
    ACTIVE = (
        (0, 'False'),
        (1, 'True')
    )
    name = models.CharField(max_length=32, unique=True, verbose_name='项目名称')
    description = models.TextField(blank=True, null=True, verbose_name='项目描述')
    is_active = models.SmallIntegerField(choices=ACTIVE, default=1, verbose_name='项目状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name


class ProjectCRUD:

    @staticmethod
    def add_project(post) -> Project:
        return Project.objects.create(**post.dict())

    @staticmethod
    def get_all_projects() -> list:
        return Project.objects.all()

    @staticmethod
    def get_project_name(post: str) -> bool:
        return Project.objects.filter(name=post)

    @staticmethod
    def get_project_name_by_id(pk: int) -> str:
        return Project.objects.filter(id=pk).first().name

    @staticmethod
    def get_project_by_id(pk: int) -> Project:
        return get_object_or_404(Project, id=pk)

    @staticmethod
    def get_project_status(pk: int) -> bool:
        return Project.objects.filter(id=pk).first().is_active
