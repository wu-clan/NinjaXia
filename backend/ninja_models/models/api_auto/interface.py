#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import get_object_or_404

from backend.ninja_models.models.api_auto.project import Project


class Interface(models.Model):
    """
    接口组
    """
    name = models.CharField(max_length=32, verbose_name='接口组名称')
    description = models.TextField(blank=True, null=True, verbose_name='接口组描述')
    project = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name


class InterfaceCRUD:

    @staticmethod
    def get_interface_by_name(name: str) -> bool:
        return Interface.objects.filter(name=name)

    @staticmethod
    def get_interface_name_by_id(pk: int) -> str:
        return Interface.objects.filter(id=pk).first().name

    @staticmethod
    def get_project_for_interface(pk: int) -> Project:
        return get_object_or_404(Project, id=pk)

    @staticmethod
    def create_interface(post, pt: int) -> Interface:
        return Interface.objects.create(**post.dict(), project_id=pt)

    @staticmethod
    def get_interface_by_id(pk: int) -> bool:
        return Interface.objects.filter(id=pk)

    @staticmethod
    def get_interface(pk: int):
        return get_object_or_404(Interface, id=pk)

    @staticmethod
    def get_all_interfaces() -> list:
        return Interface.objects.all()
