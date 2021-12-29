#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.api_auto.interface import Interface


class Case(models.Model):
    """
    用例表
    """
    TYPE = (
        (0, 'params'),
        (1, 'json'),
        (2, 'x-www-form-urlencoded')
    )
    REQUEST_TYPE = (
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE'),
    )
    ASSERT_TYPE = (
        (0, 'nothing'),  # 不断言
        (1, 'contains'),  # 包含
        (2, 'matches')  # 比较
    )
    interface_id = models.ForeignKey(Interface, verbose_name='所属接口组', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, verbose_name='用例名称')
    description = models.TextField(blank=True, null=True, verbose_name='用例描述')
    url = models.CharField(max_length=255, verbose_name='请求地址')
    method = models.SmallIntegerField(choices=REQUEST_TYPE, default=0, verbose_name='请求类型')
    header = models.TextField(blank=True, null=True, verbose_name='请求头')
    body_type = models.SmallIntegerField(choices=TYPE, default=0, verbose_name='请求参数类型')
    body = models.TextField(blank=True, null=True, verbose_name='请求参数内容')
    assert_type = models.SmallIntegerField(choices=ASSERT_TYPE, default=0, verbose_name='断言类型')
    assert_result = models.TextField(verbose_name='断言结果')
    response = models.JSONField(blank=True, null=True, default=dict, verbose_name='响应内容')

    def __str__(self):
        return self.name


class CaseCRUD:
    pass
