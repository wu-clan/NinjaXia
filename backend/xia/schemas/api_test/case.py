#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema
from pydantic import validator

from backend.xia.common.response.response_schema import Response200
from backend.xia.enums.request.body import BodyType
from backend.xia.enums.request.method import MethodType
from backend.xia.schemas.api_test.env import GetAllApiTestEnvs
from backend.xia.schemas.api_test.module import GetAllApiTestModules


class ApiTestCaseBase(Schema):
    name: str
    description: str = None
    url: str
    method: str
    params: str = None
    headers: str = None
    cookies: str = None
    body_type: int = 0
    body: str = None
    assert_text: str = None
    timeout: int = 10

    @validator('method')
    def check_method(cls, v):
        if v.upper() not in MethodType._value2member_map_:  # noqa
            raise ValueError('method value error')
        return v

    @validator('body_type')
    def check_body_type(cls, v):
        if v not in BodyType._value2member_map_:  # noqa
            raise ValueError('body_type value error')
        return v

    @validator('headers')
    def check_headers(cls, v):
        if v is not None:
            if len(eval(v)) == 0:
                raise ValueError('headers value error')
        return v


class CreateApiTestCase(ApiTestCaseBase):
    api_module: int
    api_environment: int


class UpdateApiTestCase(ApiTestCaseBase):
    api_module: int
    api_environment: int


class GetAllApiTestCases(ApiTestCaseBase):
    id: int
    api_module: GetAllApiTestModules = None
    api_environment: GetAllApiTestEnvs = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime


class ExtraDebugArgs(Schema):
    is_write_report: bool = False


class ApiTestCaseResponse(Response200):
    data: GetAllApiTestCases = None
