#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.api_auto.task import Task


class Result(models.Model):
    """
    测试结果表
    """
    task_id = models.ForeignKey(Task, verbose_name='关联任务', on_delete=models.CASCADE)
    name = models.CharField(blank=True, default='', verbose_name='测试报告名称')
    error_num = models.CharField(blank=True, null=True, max_length=100, verbose_name='失败总数')
    pass_num = models.CharField(blank=True, null=True, max_length=100, verbose_name='成功总数')
    api_number = models.CharField(blank=True, null=True, max_length=100, verbose_name='API总数')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_add=True, verbose_name='修改时间')

    def __str__(self):
        return self.name


class ResultCRUD:
    pass
