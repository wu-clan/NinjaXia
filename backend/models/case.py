#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from asgiref.sync import sync_to_async
from django.db import models

from .project import Project


class Cases(models.Model):
    """
    用例表
    """
    name = models.CharField(max_length=32, verbose_name='用例名称')
    description = models.TextField(null=True, verbose_name='用例描述')
    url = models.CharField(max_length=255, verbose_name='请求url')
    REQUEST_TYPE = (
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE'),
    )
    method = models.SmallIntegerField(choices=REQUEST_TYPE, default=0, verbose_name='请求类型')
    params = models.CharField(max_length=255, default={}, verbose_name='请求params')
    data = models.CharField(max_length=255, default={}, verbose_name='请求data')
    run_time = models.DateTimeField(auto_now_add=True, verbose_name='运行时间')
    RUN_STATUS = (
        (0, '失败'),
        (1, '通过'),
    )
    result = models.SmallIntegerField(choices=RUN_STATUS, default=0, verbose_name='执行结果')
    report = models.TextField(null=True, verbose_name='测试报告')
    project_id = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


@sync_to_async
def get_all() -> list:
    return Cases.objects.all()
