#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import List

from ninja import Schema
from pydantic import validator

from backend.schemas import Response200
from backend.schemas.sm_api_test.sm_api_test_business import GetAllApiTestBusinesses
from backend.schemas.sm_api_test.sm_api_test_project import GetAllApiTestProjects
from backend.schemas.sm_sys.sm_sys_crontab import GetAllCornTabs


class ApiTestTaskBase(Schema):
    name: str
    description: str = None
    priority: str
    start_data: datetime.datetime
    end_date: datetime.datetime
    send_report: bool
    status: bool
    execute_target: int
    retry_num: int
    api_case: List[int] = None

    @validator('priority')
    def check_priority(cls, value):
        if value not in ['P1', 'P2', 'P3', 'P4']:
            raise ValueError('priority param error')
        return value

    @validator('execute_target')
    def check_execute_target(cls, value):
        if value not in [0, 1]:
            raise ValueError('execute_target param error')
        return value

    @validator('retry_num')
    def check_retry_num(cls, value):
        if value > 10:
            raise ValueError('retry_num param error')
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
    sys_corn: GetAllCornTabs = None
    api_project: GetAllApiTestProjects = None
    api_business_test: GetAllApiTestBusinesses = None
    creator: str = None
    modifier: str = None
    created_time: datetime.datetime
    modified_time: datetime.datetime

    @staticmethod
    def resolve_api_case(value):
        return list(map(int, str(value.api_case).split(',')))


class ApiTestTaskResponse(Response200):
    data: GetAllApiTestTasks = None
