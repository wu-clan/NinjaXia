#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import Any, Union

from ninja import Schema
from pydantic import Json

from backend.xia.schemas.api_test.case import GetAllApiTestCases
from backend.xia.schemas.api_test.task import GetAllApiTestTasks


class ApiTestReportBase(Schema):
    name: str
    total_num: int = None
    pass_num: int = None
    error_num: int = None
    fail_num: int = None


class CreateApiTestReport(ApiTestReportBase):
    ...


class UpdateApiTestReport(ApiTestReportBase):
    ...


class GetAllApiTestReports(ApiTestReportBase):
    id: int
    api_task: GetAllApiTestTasks = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime


class ApiTestReportDetailBase(Schema):
    name: str
    url: str
    method: str = None
    params: str = None
    headers: str = None
    body: str = None
    status_code: int = None
    response_data: str = None
    execute_time: datetime.datetime = None
    elapsed: float
    assert_result: str = None
    run_status: str


class CreateApiTestReportDetail(ApiTestReportDetailBase):
    api_case: int


class UpdateApiTestReportDetail(ApiTestReportDetailBase):
    api_case: int


class GetAllApiTestReportsDetail(ApiTestReportDetailBase):
    id: int
    params: Json = None
    headers: Json = None
    response_data: Json = None
    body: Union[Json, Any, None] = None
    api_case: GetAllApiTestCases = None
    api_report: GetAllApiTestReports = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime
