#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.base import BaseModel
from backend.ninja_models.models.api_test.api_test_task import ApiTestTask


class ApiTestReport(BaseModel):
    """
    测试报告表
    """
    name = models.CharField(max_length=128, verbose_name='测试报告名称')
    error_num = models.BigIntegerField(null=True, verbose_name='失败总数')
    pass_num = models.BigIntegerField(null=True, verbose_name='成功总数')
    api_number = models.BigIntegerField(null=True, verbose_name='API总数')
    api_task = models.ForeignKey(ApiTestTask, on_delete=models.CASCADE, verbose_name='所属任务',
                                 related_name='api_test_report', related_query_name='api_test_report')

    class Meta:
        db_table = 'sys_api_test_report'

    def __str__(self):
        return self.name


class ApiTestReportDetail(BaseModel):
    """
    API测试报告详情表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='测试用例名称')
    business_test_name = models.CharField(max_length=128, verbose_name='业务测试名称')
    url = models.TextField(verbose_name='测试用例请求URL')
    method = models.CharField(max_length=128, verbose_name='测试用例请求方法')
    body = models.TextField(null=True, verbose_name='测试用例请求参数')
    headers = models.TextField(null=True, verbose_name='测试用例请求头')
    status_code = models.IntegerField(null=True, verbose_name='测试用例返回状态码')
    response_data = models.TextField(null=True, verbose_name='测试用例返回数据')
    assert_result = models.TextField(null=True, verbose_name='测试用例断言结果')
    api_task = models.ForeignKey(ApiTestTask, on_delete=models.CASCADE, verbose_name='所属任务',
                                 related_name='api_test_report_detail', related_query_name='api_test_report_detail')
    api_report = models.ForeignKey(ApiTestReport, on_delete=models.CASCADE, verbose_name='所属报告',
                                   related_name='api_test_report_detail', related_query_name='api_test_report_detail')

    class Meta:
        db_table = 'sys_api_test_report_detail'

    def __str__(self):
        return self.name
