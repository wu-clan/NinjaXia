#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.base import BaseModel
from backend.ninja_models.models.api_test.api_test_case import ApiTestCase
from backend.ninja_models.models.api_test.api_test_module import ApiTestModule


class ApiTestBusinessTest(BaseModel):
    """
    API业务测试表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='业务测试操作名称')
    description = models.TextField(null=True, verbose_name='业务测试操作描述')
    api_module = models.ForeignKey(ApiTestModule, on_delete=models.SET_NULL, null=True, verbose_name='所属模块',
                                   related_name='api_test_business_test',
                                   related_query_name='api_test_business_test')
    api_case = models.ForeignKey(ApiTestCase, on_delete=models.CASCADE, verbose_name='拥有测试用例',
                                 related_name='api_test_business_test',
                                 related_query_name='api_test_business_test')

    class Meta:
        db_table = 'sys_api_test_business_test'

    def __str__(self):
        return self.name
