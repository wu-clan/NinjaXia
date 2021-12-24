#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


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
    params = models.CharField(max_length=255, default={}, verbose_name='请求参数')
