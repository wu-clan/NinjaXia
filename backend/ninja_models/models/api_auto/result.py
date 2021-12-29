#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.api_auto.task import Task


class Result(models.Model):
    """
    测试结果表
    """
    task_id = models.ForeignKey(Task, verbose_name='关联任务', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True, default='', verbose_name='测试报告名称')
    error_num = models.BigIntegerField(blank=True, null=True, verbose_name='失败总数')
    pass_num = models.BigIntegerField(blank=True, null=True, verbose_name='成功总数')
    api_number = models.BigIntegerField(blank=True, null=True, verbose_name='API总数')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name


class ResultCRUD:
    pass
