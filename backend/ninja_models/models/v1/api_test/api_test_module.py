#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class ApiTestModule(models.Model):
    """
    API模块表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='模块名称')
    description = models.TextField(null=True, verbose_name='模块描述')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    api_project = models.ForeignKey('ApiTestProject', on_delete=models.CASCADE, verbose_name='所属项目')

    class Meta:
        db_table = 'sys_api_test_module'

    def __str__(self):
        return self.name
