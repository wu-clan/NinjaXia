#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.v1.api_test.api_test_environment import ApiTestEnvironment
from backend.ninja_models.models.v1.api_test.api_test_module import ApiTestModule


class ApiTestCase(models.Model):
    """
    用例表
    """
    METHOD_TYPE = (
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE'),
    )
    BODY_TYPE = (
        (0, 'none'),
        (1, 'form-data'),
        (2, 'x-www-form-urlencoded'),
        (3, 'Text'),
        (4, 'JavaScript'),
        (5, 'JSON'),
        (6, 'HTML'),
        (7, 'XML'),
    )
    ASSERT_TYPE = (
        (0, 'nothing'),  # 不断言
        (1, 'contains'),  # 包含
        (2, 'matches')  # 比较
    )
    name = models.CharField(max_length=128, unique=True, verbose_name='用例名称')
    description = models.TextField(null=True, verbose_name='用例描述')
    url = models.TextField(verbose_name='请求URL')
    method = models.SmallIntegerField(choices=METHOD_TYPE, default=0, verbose_name='请求方法')
    headers = models.TextField(null=True, verbose_name='请求头')
    body_type = models.SmallIntegerField(choices=BODY_TYPE, default=0, verbose_name='请求参数类型')
    body = models.TextField(null=True, verbose_name='请求参数')
    assert_type = models.SmallIntegerField(choices=ASSERT_TYPE, default=0, verbose_name='断言类型')
    assert_text = models.TextField(verbose_name='断言内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    api_module = models.ForeignKey(ApiTestModule, on_delete=models.CASCADE, verbose_name='所属模块',
                                   related_name='api_test_case', related_query_name='api_test_case')
    api_environment = models.ForeignKey(ApiTestEnvironment, on_delete=models.CASCADE, verbose_name='所属环境',
                                        related_name='api_test_case', related_query_name='api_test_case')

    class Meta:
        db_table = 'sys_api_test_case'

    def __str__(self):
        return self.name
