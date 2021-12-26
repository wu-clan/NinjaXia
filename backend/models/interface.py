#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.models.project import Project


class Interface(models.Model):
    """
    接口表
    """
    name = models.CharField(max_length=32, verbose_name='接口名称')
    description = models.TextField(blank=True, null=True, verbose_name='接口描述')
    REQUEST_TYPE = (
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE'),
    )
    method = models.SmallIntegerField(choices=REQUEST_TYPE, default=0, verbose_name='请求类型')
    url = models.CharField(max_length=255, verbose_name='请求url')
    project_id = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class InterfaceCRUD:
    pass
