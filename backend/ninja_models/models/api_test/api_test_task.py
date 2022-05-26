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
    cron = models.CharField(max_length=32, verbose_name='cron表达式')
    priority = models.CharField(max_length=32, verbose_name='优先级')
    starting_time = models.DateTimeField(max_length=64, verbose_name='起始时间')
    end_time = models.DateTimeField(max_length=64, verbose_name='截至时间')
    time_interval_day = models.IntegerField(default=1, verbose_name='间隔时间-天')
    time_interval_hours = models.IntegerField(default=0, verbose_name='间隔时间-小时')
    time_interval_minutes = models.IntegerField(default=0, verbose_name='间隔时间-分钟')
    time_interval_seconds = models.IntegerField(default=0, verbose_name='间隔时间-秒')
    send_report = models.IntegerField(default=0, verbose_name='发送测试报告')
    status = models.BooleanField(default=1, verbose_name='任务状态')
    state = models.CharField(max_length=32, verbose_name='任务运行状态')
    execute_target = models.SmallIntegerField(default=0, verbose_name='执行目标, 0: 业务, 1: 用例')
    retry = models.IntegerField(default=0, verbose_name='重试次数')
    api_case = models.CharField(max_length=256, null=True, verbose_name='拥有测试用例')
    api_project = models.ForeignKey(ApiTestProject, on_delete=models.SET_NULL, null=True, verbose_name='所属项目',
                                    related_name='api_test_tasks', related_query_name='api_test_task')
    api_business_test = models.ForeignKey(ApiTestBusinessTest, on_delete=models.SET_NULL, null=True,
                                          verbose_name='拥有业务测试', related_name='api_test_tasks',
                                          related_query_name='api_test_task')

    class Meta:
        db_table = 'sys_api_test_task'

    def __str__(self):
        return self.name
