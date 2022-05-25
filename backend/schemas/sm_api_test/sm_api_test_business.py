#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import List

from ninja import Schema

from backend.schemas import Response200
from backend.schemas.sm_api_test.sm_api_test_case import GetAllApiTestCases
from backend.schemas.sm_api_test.sm_api_test_module import GetAllApiTestModules


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
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime


class GetAllApiTestBusinessesAndCases(ApiTestBusinessBaseAndCase):
    id: int
    api_business_test: GetAllApiTestBusinesses = None
    api_case: GetAllApiTestCases = None
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime


class BusinessesAndCasesResponse(Response200):
    data: List[GetAllApiTestBusinessesAndCases] = None
