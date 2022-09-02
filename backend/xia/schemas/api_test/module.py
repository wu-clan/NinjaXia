#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema

from backend.xia.common.response.response_schema import Response200
from backend.xia.schemas.api_test.project import GetAllApiTestProjects


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


class ApiTestModuleResponse(Response200):
    data: GetAllApiTestModules = None
