#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.xia.models.api_test.business_test import ApiTestBusinessTest
from backend.xia.models.api_test.project import ApiTestProject
from backend.xia.models.sys.crontab import SysCrontab
from backend.xia.models.base import BaseModel


class ApiTestTask(BaseModel):
    """
    任务表
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='测试任务名称')
    description = models.TextField(null=True, verbose_name='任务描述')
    priority = models.CharField(max_length=32, verbose_name='优先级')
    start_data = models.DateTimeField(max_length=64, verbose_name='起始时间')
    end_date = models.DateTimeField(max_length=64, verbose_name='截至时间')
    send_report = models.BooleanField(default=0, verbose_name='发送测试报告, 0:不发送, 1:发送')
    status = models.BooleanField(default=1, verbose_name='任务状态')
    state = models.IntegerField(default=0, verbose_name='任务运行状态, 0: 未执行, 1: 等待执行, 2: 执行中, 3: 暂停')
    execute_target = models.IntegerField(default=0, verbose_name='执行目标, 0: 业务, 1: 用例')
    retry_num = models.IntegerField(default=0, verbose_name='重试次数')
    api_case = models.CharField(max_length=256, null=True, verbose_name='拥有测试用例')
    sys_cron = models.ForeignKey(
        SysCrontab,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='所属定时器',
        related_name='api_test_tasks',
        related_query_name='api_test_task'
    )
    api_project = models.ForeignKey(
        ApiTestProject,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='所属项目',
        related_name='api_test_tasks',
        related_query_name='api_test_task'
    )
    api_business_test = models.ForeignKey(
        ApiTestBusinessTest,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='拥有业务测试',
        related_name='api_test_tasks',
        related_query_name='api_test_task'
    )

    class Meta:
        db_table = 'sys_api_test_task'

    def __str__(self):
        return self.name
