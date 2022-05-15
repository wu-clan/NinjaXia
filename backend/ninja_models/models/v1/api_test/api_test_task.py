#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.v1.api_test.api_test_project import ApiTestProject


class ApiTestTask(models.Model):
    """
    任务表
    """
    STATUS = (
        (0, '未执行'),
        (1, '排队中'),
        (2, '执行中'),
        (3, '执行完成')
    )
    name = models.CharField(max_length=128, unique=True, verbose_name='测试任务名称')
    description = models.TextField(null=True, verbose_name='任务描述')
    status = models.SmallIntegerField(choices=STATUS, default=0, verbose_name='任务状态')
    cases = models.TextField(default="", verbose_name='关联API用例')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    api_project = models.ForeignKey(ApiTestProject, verbose_name='关联项目', on_delete=models.CASCADE,
                                    related_name='api_test_tasks', related_query_name='api_test_task')

    class Meta:
        db_table = 'sys_api_test_task'

    def __str__(self):
        return self.name
