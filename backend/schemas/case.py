#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import IntEnum

from ninja import Schema
from pydantic import Field


class CaseMethod(IntEnum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3


class CaseBody(IntEnum):
    params = 0
    json = 1
    x_www_form_urlencoded = 2


class CaseAssert(IntEnum):
    nothing = 0
    contains = 1
    matches = 2


class CaseBase(Schema):
    name: str
    description: str = None
    url: str
    method: CaseMethod = Field(default=CaseMethod.GET, description='请求类型')
    header: str = None
    body_type: CaseBody = Field(default=CaseBody.json, description='请求体')
    body: str = None
    assert_type: CaseAssert = Field(default=CaseAssert.nothing, description='断言类型')
    assert_result: str


class CreateCase(Schema):
    id: int = Field(default=1, description='接口组主键')


class UpdateCase(CreateCase):
    pass


class GetCase(CaseBase):
    id: int
