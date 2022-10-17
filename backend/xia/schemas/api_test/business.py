#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import List

from ninja import Schema

from backend.xia.common.response.response_schema import Response200
from backend.xia.schemas.api_test.case import GetAllApiTestCases
from backend.xia.schemas.api_test.module import GetAllApiTestModules


class ApiTestBusinessBase(Schema):
    name: str
    description: str = None


class ApiTestBusinessBaseAndCase(Schema):
    api_business_test: int
    api_case: int


class CreateApiTestBusiness(ApiTestBusinessBase):
    api_module: int
    api_cases: List[int] = []


class UpdateApiTestBusiness(ApiTestBusinessBase):
    api_module: int
    api_cases: List[int] = []


class GetAllApiTestBusinesses(ApiTestBusinessBase):
    id: int
    api_module: GetAllApiTestModules = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime


class GetAllApiTestBusinessesAndCases(ApiTestBusinessBaseAndCase):
    id: int
    api_business_test: GetAllApiTestBusinesses = None
    api_case: GetAllApiTestCases = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime


class BusinessesAndCasesResponse(Response200):
    data: List[GetAllApiTestBusinessesAndCases] = None
