#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class ApiEnvironment(models.Model):
    """
    API环境表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='环境名称')
    description = models.TextField(null=True, verbose_name='环境描述')
    status = models.BooleanField(default=1, verbose_name='环境状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'sys_api_environment'

    def __str__(self):
        return self.name
