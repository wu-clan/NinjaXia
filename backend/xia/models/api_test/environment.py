#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.xia.models.base import BaseModel


class ApiTestEnvironment(BaseModel):
    """
    API环境表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='环境名称')
    host = models.CharField(max_length=128, verbose_name='环境地址')
    description = models.TextField(null=True, verbose_name='环境描述')
    status = models.BooleanField(default=1, verbose_name='环境状态')

    class Meta:
        db_table = 'sys_api_test_environment'

    def __str__(self):
        return self.name
