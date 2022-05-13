#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


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
        (0, 'params'),
        (1, 'json'),
        (2, 'x-www-form-urlencoded')
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
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    api_model = models.ForeignKey('ApiTestModule', on_delete=models.CASCADE, verbose_name='所属模块')
    api_environment = models.ForeignKey('ApiTestEnvironment', on_delete=models.CASCADE, verbose_name='所属环境')

    class Meta:
        db_table = 'sys_api_test_case'

    def __str__(self):
        return self.name
