#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema

from backend.xia.common.response.response_schema import ResponseModel
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
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime


class GetOneApiTestModuleResponse(ResponseModel):
    data: GetAllApiTestModules = None
