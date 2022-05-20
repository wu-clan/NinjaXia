#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema


class ApiTestProjectBase(Schema):
    name: str
    description: str = None
    status: bool


class CreateApiTestProject(ApiTestProjectBase):
    pass


class UpdateApiTestProject(ApiTestProjectBase):
    name: str = None


class GetAllApiTestProjects(ApiTestProjectBase):
    id: int
    created_time: datetime.datetime
    modified_time: datetime.datetime
