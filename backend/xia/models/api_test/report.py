#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.xia.models.api_test.case import ApiTestCase
from backend.xia.models.api_test.task import ApiTestTask
from backend.xia.models.base import BaseModel


class ApiTestReport(BaseModel):
    """
    测试报告表
    """
    name = models.CharField(max_length=128, verbose_name='测试报告名称')
    total_num = models.BigIntegerField(default=0, null=True, verbose_name='用例总数')
    pass_num = models.BigIntegerField(default=0, null=True, verbose_name='成功总数')
    error_num = models.BigIntegerField(default=0, null=True, verbose_name='错误总数')
    fail_num = models.BigIntegerField(default=0, null=True, verbose_name='失败总数')
    api_task = models.ForeignKey(ApiTestTask, on_delete=models.CASCADE, verbose_name='所属任务',
                                 related_name='api_test_reports', related_query_name='api_test_report')

    class Meta:
        db_table = 'sys_api_test_report'

    def __str__(self):
        return self.name


class ApiTestReportDetail(BaseModel):
    """
    API测试报告详情表
    """
    name = models.CharField(max_length=128, verbose_name='用例名称')
    url = models.TextField(verbose_name='用例请求URL')
    method = models.CharField(max_length=128, verbose_name='用例请求方法')
    params = models.TextField(null=True, verbose_name='用例查询参数')
    headers = models.TextField(null=True, verbose_name='用例请求头')
    body = models.TextField(null=True, verbose_name='用例请求参数')
    status_code = models.IntegerField(null=True, verbose_name='用例响应状态码')
    response_data = models.TextField(null=True, verbose_name='用例响应结果')
    execute_time = models.DateTimeField(null=True, verbose_name='执行时间')
    elapsed = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='响应时长(ms)')
    assert_result = models.TextField(null=True, verbose_name='用例断言结果')
    run_status = models.CharField(max_length=32, default='FAIL', verbose_name='执行状态')
    api_case = models.ForeignKey(ApiTestCase, on_delete=models.CASCADE, verbose_name='所属用例',
                                 related_name='api_test_report_details', related_query_name='api_test_report_detail')
    api_report = models.ForeignKey(ApiTestReport, on_delete=models.CASCADE, null=True, verbose_name='所属报告',
                                   related_name='api_test_report_details', related_query_name='api_test_report_detail')

    class Meta:
        db_table = 'sys_api_test_report_detail'

    def __str__(self):
        return self.name
