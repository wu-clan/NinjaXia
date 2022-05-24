#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema

from backend.schemas.sm_api_test.sm_api_test_project import GetAllApiTestProjects


class ApiTestModuleBase(Schema):
    name: str
    description: str = None


class CreateApiTestModule(ApiTestModuleBase):
    api_project: int


class UpdateApiTestModule(ApiTestModuleBase):
    api_project: int


class GetAllApiTestModules(ApiTestModuleBase):
    id: int
    api_project: GetAllApiTestProjects = None
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime
