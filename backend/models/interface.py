#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.models.project import Project


class Interface(models.Model):
    """
    接口组
    """
    name = models.CharField(max_length=32, verbose_name='接口组名称')
    description = models.TextField(blank=True, null=True, verbose_name='接口组描述')
    project_id = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class InterfaceCRUD:
    pass
