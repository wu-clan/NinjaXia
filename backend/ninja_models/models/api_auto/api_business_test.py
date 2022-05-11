#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class ApiBusinessTest(models.Model):
    """
    API业务测试表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='业务测试名称')
    description = models.TextField(null=True, verbose_name='业务测试描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    api_project = models.ForeignKey('ApiProject', on_delete=models.CASCADE, verbose_name='所属项目')

    class Meta:
        db_table = 'sys_api_business_test'

    def __str__(self):
        return self.name


class ApiBusinessTestAssociated(models.Model):
    """
    API业务测试关联表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='操作名称')
    description = models.TextField(null=True, verbose_name='操作描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    api_business_test = models.ForeignKey(ApiBusinessTest, on_delete=models.CASCADE, verbose_name='所属业务测试')
    api_module = models.ForeignKey('ApiModule', on_delete=models.CASCADE, verbose_name='所属模块')
    api_test_case = models.ForeignKey('ApiTestCase', on_delete=models.CASCADE, verbose_name='所属测试用例')

    class Meta:
        db_table = 'sys_api_business_test_associated'

    def __str__(self):
        return self.name
