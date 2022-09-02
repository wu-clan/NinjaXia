#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.xia.models.base import BaseModel


class ApiTestProject(BaseModel):
    """
    API项目表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='项目名称')
    description = models.TextField(null=True, verbose_name='项目描述')
    status = models.BooleanField(default=1, verbose_name='项目状态')

    class Meta:
        db_table = 'sys_api_test_project'

    def __str__(self):
        return self.name
