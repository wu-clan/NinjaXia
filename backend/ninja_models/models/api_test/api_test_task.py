#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models import ApiTestBusinessTest
from backend.ninja_models.models.base import BaseModel
from backend.ninja_models.models.api_test.api_test_project import ApiTestProject


class ApiTestTask(BaseModel):
    """
    任务表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='测试任务名称')
    description = models.TextField(null=True, verbose_name='任务描述')
    starting_time = models.CharField(max_length=64, default='', verbose_name='起始时间')
    end_time = models.CharField(max_length=64, default='', verbose_name='截至时间')
    time_interval_day = models.IntegerField(default=0, verbose_name='间隔时间-天')
    time_interval_hours = models.IntegerField(default=0, verbose_name='间隔时间-小时')
    time_interval_minutes = models.IntegerField(default=0, verbose_name='间隔时间-分钟')
    time_interval_seconds = models.IntegerField(default=0, verbose_name='间隔时间-秒')
    is_enable = models.BooleanField(default=1, verbose_name='是否启用任务')
    is_send_email = models.BooleanField(default=1, verbose_name='是否发送邮件测试报告')
    status = models.CharField(max_length=32, verbose_name='任务运行状态')
    api_project = models.ForeignKey(ApiTestProject, on_delete=models.SET_NULL, null=True, verbose_name='所属项目',
                                    related_name='api_test_tasks', related_query_name='api_test_task')
    api_business_test = models.ForeignKey(ApiTestBusinessTest, on_delete=models.CASCADE, verbose_name='拥有业务测试',
                                          related_name='api_test_tasks', related_query_name='api_test_task')

    class Meta:
        db_table = 'sys_api_test_task'

    def __str__(self):
        return self.name
