#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import List

from ninja import Schema
from pydantic import validator, Field

from backend.xia.common.response.response_schema import Response200
from backend.xia.enums.task_execute_target import ExecuteTargetType
from backend.xia.enums.task_priority import PriorityType
from backend.xia.schemas.api_test.business import GetAllApiTestBusinesses
from backend.xia.schemas.api_test.project import GetAllApiTestProjects
from backend.xia.schemas.sys.crontab import GetAllCornTabs


class ApiTestTaskBase(Schema):
    name: str
    description: str = None
    priority: str
    start_data: datetime.datetime
    end_date: datetime.datetime
    send_report: bool
    status: bool
    execute_target: int
    retry_num: int = Field(..., ge=0, le=10)
    api_case: List[int] = None

    @validator('priority')
    def check_priority(cls, value):
        if value not in PriorityType._value2member_map_:  # noqa
            raise ValueError('priority param error')
        return value

    @validator('execute_target')
    def check_execute_target(cls, value):
        if value not in ExecuteTargetType._value2member_map_:  # noqa
            raise ValueError('execute_target param error')
        return value


class CreateApiTestTask(ApiTestTaskBase):
    sys_cron: int
    api_project: int
    api_business_test: int


class UpdateApiTestTask(ApiTestTaskBase):
    sys_cron: int
    api_project: int
    api_business_test: int


class GetAllApiTestTasks(ApiTestTaskBase):
    id: int
    state: int
    sys_cron: GetAllCornTabs = None
    api_project: GetAllApiTestProjects = None
    api_business_test: GetAllApiTestBusinesses = None
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime

    @staticmethod
    def resolve_api_case(value):
        if value.api_case is not None:
            if len(value.api_case) > 0:
                return list(map(int, str(value.api_case).split(',')))
        return


class ApiTestTaskResponse(Response200):
    data: GetAllApiTestTasks = None
