#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.base import BaseModel


class Crontab(BaseModel):
    """
    定时任务
    """
    second = models.CharField(max_length=32, verbose_name='一分钟某秒')
    minute = models.CharField(max_length=32, verbose_name='一小时某分')
    hour = models.CharField(max_length=32, verbose_name='一天某小时')
    day = models.CharField(max_length=32, verbose_name='一月中某日')
    month = models.CharField(max_length=32, verbose_name='一年中某月')
    day_of_week = models.CharField(max_length=32, verbose_name='一周的某一天')

    class Meta:
        db_table = 'sys_crontab'

    def __str__(self):
        return self.second
