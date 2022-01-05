#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import models
from django.shortcuts import get_object_or_404

from backend.ninja_models.models.api_auto.interface import Interface
from backend.schemas.case import CaseBase


class Case(models.Model):
    """
    用例表
    """
    METHOD_TYPE = (
        (0, 'GET'),
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE'),
    )
    BODY_TYPE = (
        (0, 'params'),
        (1, 'json'),
        (2, 'x-www-form-urlencoded')
    )
    ASSERT_TYPE = (
        (0, 'nothing'),  # 不断言
        (1, 'contains'),  # 包含
        (2, 'matches')  # 比较
    )
    interface = models.ForeignKey(Interface, verbose_name='所属接口组', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, unique=True, verbose_name='用例名称')
    description = models.TextField(blank=True, null=True, verbose_name='用例描述')
    url = models.CharField(max_length=255, verbose_name='请求地址')
    method = models.SmallIntegerField(choices=METHOD_TYPE, default=0, verbose_name='请求类型')
    header = models.TextField(blank=True, null=True, verbose_name='请求头')
    body_type = models.SmallIntegerField(choices=BODY_TYPE, default=0, verbose_name='请求参数类型')
    body = models.TextField(blank=True, null=True, verbose_name='请求参数内容')
    assert_type = models.SmallIntegerField(choices=ASSERT_TYPE, default=0, verbose_name='断言类型')
    assert_result = models.TextField(verbose_name='断言结果')

    def __str__(self):
        return self.name


class CaseCRUD:

    @staticmethod
    def get_case_by_name(name: str) -> bool:
        return Case.objects.filter(name=name)

    @staticmethod
    def get_case_by_id(pk: int):
        return get_object_or_404(Case, id=pk)

    @staticmethod
    def get_case_name_by_id(pk: id) -> str:
        return Case.objects.filter(id=pk).first().name
    
    @staticmethod
    def create_case(post: CaseBase, iid: int) -> Case:
        return Case.objects.create(**post.dict(), interface_id=iid)

    @staticmethod
    def get_interface_for_case(pk: int) -> Interface:
        return get_object_or_404(Interface, id=pk)

    @staticmethod
    def get_all_cases() -> list:
        return Case.objects.all()

