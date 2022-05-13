#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Optional

from ninja import Schema


class ApiTestModuleBase(Schema):
    name: str
    description: Optional[str]


class CreateApiTestModule(ApiTestModuleBase):
    api_project: int


class UpdateApiTestModule(ApiTestModuleBase):
    api_project: int


class GetAllApiTestModules(ApiTestModuleBase):
    id: int
    api_project: int
    created_time: datetime.datetime
    modified_time: datetime.datetime
