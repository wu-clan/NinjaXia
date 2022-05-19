#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Optional

from ninja import Schema


class ApiTestEnvBase(Schema):
    name: str
    description: Optional[str]
    status: bool


class CreateApiTestEnv(ApiTestEnvBase):
    ...


class UpdateApiTestEnv(ApiTestEnvBase):
    ...


class GetAllApiTestEnv(ApiTestEnvBase):
    id: int
    created_time: datetime.datetime
    modified_time: datetime.datetime
