#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.xia.models.base import BaseModel
from backend.xia.models.api_test.project import ApiTestProject


class ApiTestModule(BaseModel):
    """
    API模块表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='模块名称')
    description = models.TextField(null=True, verbose_name='模块描述')
    api_project = models.ForeignKey(
        ApiTestProject,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='所属项目',
        related_name='api_test_modules',
        related_query_name='api_test_module'
    )

    class Meta:
        db_table = 'sys_api_test_module'

    def __str__(self):
        return self.name
