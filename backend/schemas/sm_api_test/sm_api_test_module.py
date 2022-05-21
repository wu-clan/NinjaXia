#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema


class ApiTestModuleBase(Schema):
    name: str
    description: str = None


class CreateApiTestModule(ApiTestModuleBase):
    api_project: int


class UpdateApiTestModule(ApiTestModuleBase):
    api_project: int


class GetAllApiTestModules(ApiTestModuleBase):
    id: int
    api_project_id: int
    created_time: datetime.datetime
    modified_time: datetime.datetime
