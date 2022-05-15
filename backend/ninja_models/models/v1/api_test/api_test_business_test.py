#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.v1.api_test.api_test_case import ApiTestCase
from backend.ninja_models.models.v1.api_test.api_test_module import ApiTestModule
from backend.ninja_models.models.v1.api_test.api_test_project import ApiTestProject


class ApiTestBusinessTest(models.Model):
    """
    API业务测试表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='业务测试名称')
    description = models.TextField(null=True, verbose_name='业务测试描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    api_project = models.ForeignKey(ApiTestProject, on_delete=models.CASCADE, verbose_name='所属项目',
                                    related_name='api_test_business_tests', related_query_name='api_test_business_test')

    class Meta:
        db_table = 'sys_api_test_business_test'

    def __str__(self):
        return self.name


class ApiTestBusinessTestAssociated(models.Model):
    """
    API业务测试关联表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='操作名称')
    description = models.TextField(null=True, verbose_name='操作描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    api_business_test = models.ForeignKey(ApiTestBusinessTest, on_delete=models.CASCADE, verbose_name='所属业务测试')
    api_module = models.ForeignKey(ApiTestModule, on_delete=models.CASCADE, verbose_name='所属模块',
                                   related_name='api_test_business_test_associated',
                                   related_query_name='api_test_business_test_associated')
    api_case = models.ForeignKey(ApiTestCase, on_delete=models.CASCADE, verbose_name='所属测试用例',
                                 related_name='api_test_business_test_associated',
                                 related_query_name='api_test_business_test_associated')

    class Meta:
        db_table = 'sys_api_test_business_test_associated'

    def __str__(self):
        return self.name