# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

from backend.schemas.project import ProjectBase


class Project(models.Model):
    """
    项目管理
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='项目名称')
    description = models.TextField(blank=True, null=True, verbose_name='项目描述')
    executor = models.ForeignKey(User, verbose_name='执行者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name


class ProjectCRUD:

    @staticmethod
    def get_all_projects() -> list:
        return Project.objects.all()

    @staticmethod
    def get_project_name(post: ProjectBase) -> bool:
        return Project.objects.filter(name=post.name)

    @staticmethod
    def get_project_name_by_id(pid: int) -> str:
        return Project.objects.filter(id=pid).first().name

    @staticmethod
    def get_project_by_id(pid: int) -> Project:
        return get_object_or_404(Project, id=pid)
