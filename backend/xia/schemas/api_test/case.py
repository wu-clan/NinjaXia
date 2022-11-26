#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Union, Any

from ninja import Schema
from pydantic import validator, Json

from backend.xia.common.response.response_schema import ResponseModel
from backend.xia.enums.request.body import BodyType
from backend.xia.enums.request.method import MethodType
from backend.xia.schemas.api_test.env import GetAllApiTestEnvs
from backend.xia.schemas.api_test.module import GetAllApiTestModules


class ApiTestCaseBase(Schema):
    name: str
    description: str = None
    path: str
    method: MethodType = MethodType.GET
    params: str = None
    headers: str = None
    cookies: str = None
    body_type: BodyType = BodyType.none
    body: str = None
    assert_text: str = None
    timeout: int = 10

    @validator('method')
    def check_method(cls, v):
        if v.upper() not in MethodType.get_member_values():
            raise ValueError('请求方式错误')
        return v.upper()

    @validator('body_type')
    def check_body_type(cls, v):
        if v not in BodyType.get_member_values():
            raise ValueError('请求类型错误')
        if v == BodyType.binary:
            raise ValueError('请求类型 binary 尚未支持')
        return v


class CreateApiTestCase(ApiTestCaseBase):
    api_module: int
    api_environment: int


class UpdateApiTestCase(ApiTestCaseBase):
    api_module: int
    api_environment: int


class GetAllApiTestCases(ApiTestCaseBase):
    id: int
    params: Json = None
    headers: Json = None
    cookies: Json = None
    body: Union[Json, Any, None] = None
    api_module: GetAllApiTestModules = None
    api_environment: GetAllApiTestEnvs = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime


class ExtraDebugArgs(Schema):
    is_write_report: bool = False


class GetOneApiTestCaseResponse(ResponseModel):
    data: GetAllApiTestCases = None
