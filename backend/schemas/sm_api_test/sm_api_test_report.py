#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Any

from ninja import Schema

from backend.schemas.sm_api_test.sm_api_test_case import GetAllApiTestCases


class ApiTestReportBase(Schema):
    ...


class CreateApiTestReport(ApiTestReportBase):
    ...


class UpdateApiTestReport(ApiTestReportBase):
    ...


class GetAllApiTestReports(ApiTestReportBase):
    ...


class ApiTestReportDetailBase(Schema):
    name: str
    url: str
    method: str = None
    params: Any = None
    headers: Any = None
    body: str = None
    status_code: int = None
    response_data: Any = None
    execute_time: datetime.datetime
    elapsed: float
    assert_result: str = None
    run_status: str


class CreateApiTestReportDetail(ApiTestReportDetailBase):
    api_case: int


class UpdateApiTestReportDetail(ApiTestReportDetailBase):
    api_case: int


class GetAllApiTestReportsDetail(ApiTestReportDetailBase):
    id: int
    api_case: GetAllApiTestCases = None
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime

