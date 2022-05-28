#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import json
from typing import Any

from ninja import Schema
from pydantic import validator, Field

from backend.schemas import Response200
from backend.schemas.sm_api_test.sm_api_test_env import GetAllApiTestEnvs
from backend.schemas.sm_api_test.sm_api_test_module import GetAllApiTestModules


class ApiTestCaseBase(Schema):
    name: str
    description: str = None
    url: str
    method: str
    params: dict = None
    headers: dict = None
    body_type: str
    body: Any = None
    assert_text: Any = None

    @validator('method')
    def check_method(cls, value):
        if value not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            raise ValueError('method param error')
        return value

    @validator('body_type')
    def check_body_type(cls, value):
        if value not in ['none', 'form-data', 'x-www-form-urlencoded', 'binary', 'GraphQL', 'Text', 'JavaScript',
                         'JSON', 'HTML', 'XML']:
            raise ValueError('body_type param error')
        return value

    @validator('assert_text')
    def check_assert_text(cls, value):
        if '"' in value:
            raise ValueError('assert_text param error')
        return value


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
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime

    @validator('params')
    def loads_params(cls, value):
        return json.loads(json.dumps(value))

    @validator('headers')
    def loads_headers(cls, value):
        return json.loads(json.dumps(value))


class ExtraDebugArgs(Schema):
    cookies: dict = None
    timeout: int = Field(default=10, ge=1)
    is_write_report: bool = False


class ApiTestCaseResponse(Response200):
    data: GetAllApiTestCases = None
