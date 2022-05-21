#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema
from pydantic import validator


class ApiTestCaseBase(Schema):
    name: str
    description: str = None
    url: str
    method: str
    headers: dict = None
    body_type: str
    body: str = None
    assert_type: str
    assert_text: str = None

    @validator('method')
    def check_method(cls, value):
        if value not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
            raise ValueError('method param error')
        return value

    @validator('headers')
    def check_headers(cls, value):
        if value is None:
            return value
        if not isinstance(value, dict):
            raise ValueError('headers param must be dict')
        if not value:
            raise ValueError('headers param must not be empty')
        return value

    @validator('body_type')
    def check_body_type(cls, value):
        if value not in ['none', 'form-data', 'x-www-form-urlencoded', 'binary', 'GraphQL', 'Text', 'JavaScript',
                         'JSON', 'HTML', 'XML']:
            raise ValueError('body_type param error')
        return value

    @validator('assert_type')
    def check_assert_type(cls, value):
        if value not in ['nothing', 'status_code', 'contains', 'not_contains', 'matches']:
            raise ValueError('assert_type param error')
        return value


class CreateApiTestCase(ApiTestCaseBase):
    api_module: int
    api_environment: int


class UpdateApiTestCase(ApiTestCaseBase):
    api_module: int
    api_environment: int


class GetAllApiTestCase(ApiTestCaseBase):
    id: int
    api_module_id: int
    api_environment_id: int
    created_time: datetime.datetime
    modified_time: datetime.datetime
