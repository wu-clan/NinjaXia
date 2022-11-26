#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.xia.models.api_test.environment import ApiTestEnvironment
from backend.xia.models.api_test.module import ApiTestModule
from backend.xia.models.base import Base


class ApiTestCase(Base):
    """
    用例表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='用例名称')
    description = models.TextField(null=True, verbose_name='用例描述')
    path = models.TextField(verbose_name='请求路径')
    method = models.CharField(max_length=32, verbose_name='请求方法')
    params = models.TextField(null=True, verbose_name='查询参数')
    headers = models.TextField(null=True, verbose_name='请求头')
    cookies = models.TextField(null=True, verbose_name='cookies')
    body_type = models.IntegerField(verbose_name='请求参数类型, 0: none, 1: form, 2: x_form, 3: binary, 4: graphQL, '
                                                 '5: text, 6: js, 7: json, 8: html, 9: xml')
    body = models.TextField(null=True, verbose_name='请求参数')
    assert_text = models.TextField(null=True, verbose_name='断言内容')
    timeout = models.IntegerField(default=10, verbose_name='请求超时时长')
    api_module = models.ForeignKey(
        ApiTestModule,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='所属模块',
        related_name='api_test_cases',
        related_query_name='api_test_case'
    )
    api_environment = models.ForeignKey(
        ApiTestEnvironment,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='所属环境',
        related_name='api_test_cases',
        related_query_name='api_test_case'
    )

    class Meta:
        db_table = 'sys_api_test_case'

    def __str__(self):
        return self.name
