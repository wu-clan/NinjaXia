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


class GetAllApiTestEnvs(ApiTestEnvBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime
