#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.models.interface import Interface


class Case(models.Model):
    """
    用例表
    """
    TYPE = (
        (0, 'params'),
        (1, 'json'),
    )
    RUN_STATUS = (
        (0, '失败'),
        (1, '通过'),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name='用例名称')
    description = models.TextField(blank=True, null=True, verbose_name='用例描述')
    header = models.TextField(blank=True, null=True, verbose_name='请求头')
    body_type = models.SmallIntegerField(choices=TYPE, default=0, verbose_name='请求参数类型')
    body = models.TextField(blank=True, null=True, verbose_name='请求参数')
    response = models.JSONField(blank=True, null=True, default=dict, verbose_name='响应data')
    result = models.SmallIntegerField(choices=RUN_STATUS, default=0, verbose_name='执行结果')
    interface_id = models.ForeignKey(Interface, verbose_name='所属接口', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CaseCRUD:
    pass
