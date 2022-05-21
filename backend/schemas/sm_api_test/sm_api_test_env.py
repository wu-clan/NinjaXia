#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema
from pydantic import AnyUrl, validator


class ApiTestEnvBase(Schema):
    name: str
    host: AnyUrl
    description: str = None
    status: bool

    @validator('host')
    def check_host(cls, v):
        if not v.startswith('http'):
            raise ValueError('链接地址输入有误')
        return v


class CreateApiTestEnv(ApiTestEnvBase):
    ...


class UpdateApiTestEnv(ApiTestEnvBase):
    ...


class GetAllApiTestEnv(ApiTestEnvBase):
    id: int
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime
