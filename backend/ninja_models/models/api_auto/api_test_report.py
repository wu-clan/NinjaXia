#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class ApiTestReport(models.Model):
    """
    测试报告表
    """
    name = models.CharField(max_length=128, verbose_name='测试报告名称')
    error_num = models.BigIntegerField(null=True, verbose_name='失败总数')
    pass_num = models.BigIntegerField(null=True, verbose_name='成功总数')
    api_number = models.BigIntegerField(null=True, verbose_name='API总数')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    task = models.ForeignKey('ApiTestTask', on_delete=models.CASCADE, verbose_name='所属任务')

    class Meta:
        db_table = 'sys_api_test_report'

    def __str__(self):
        return self.name


class ApiTestReportDetail(models.Model):
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
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    api_test_task = models.ForeignKey('ApiTestTask', on_delete=models.CASCADE, verbose_name='所属任务')
    api_test_report = models.ForeignKey('ApiTestReport', on_delete=models.CASCADE, verbose_name='所属报告')
