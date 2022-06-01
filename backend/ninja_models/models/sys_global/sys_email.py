#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models

from backend.ninja_models.models.base import BaseModel


class Sender(BaseModel):
    """
    发件人
    """
    name = models.CharField(max_length=128, verbose_name='发件人名称')
    email = models.EmailField(verbose_name='发件人邮箱')
    password = models.CharField(max_length=128, verbose_name='发件人邮箱密码')
    smtp_server = models.CharField(max_length=32, verbose_name='发件服务器')
    smtp_port = models.IntegerField(verbose_name='发件服务器端口')
    is_ssl = models.BooleanField(default=False, verbose_name='是否使用SSL')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys_email_sender'


class ReceiverGroup(BaseModel):
    """
    收件人组
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='收件人组名称')
    description = models.TextField(null=True, verbose_name='收件人组描述')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys_email_receiver_group'


class Receiver(BaseModel):
    """
    收件人
    """
    name = models.CharField(max_length=128, unique=True, verbose_name='收件人名称')
    email = models.EmailField(unique=True, verbose_name='收件人邮箱')
    receiver_group = models.ForeignKey(ReceiverGroup, on_delete=models.CASCADE, verbose_name='所属收件人组',
                                       related_name='receivers', related_query_name='receiver')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys_email_receiver'
