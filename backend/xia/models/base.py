#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    """
    基本模型
    """
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    creator = models.CharField(max_length=32, null=True, verbose_name='创建者')
    modifier = models.CharField(max_length=32, null=True, verbose_name='修改者')

    class Meta:
        abstract = True
