# -*- coding: utf-8 -*-
from asgiref.sync import sync_to_async
from django.db import models


# Create your models here.

class Project(models.Model):
    """
    项目管理
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='项目名称')
    description = models.TextField(null=True, verbose_name='项目描述')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.name


@sync_to_async
def get_all() -> list:
    return Project.objects.all()



