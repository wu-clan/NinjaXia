#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models


class Base(models.Model):
    """
    基本模型
    """
    create_user = models.BigIntegerField(null=False, verbose_name='创建者')
    update_user = models.BigIntegerField(null=True, verbose_name='修改者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = ''
        abstract = True
