#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from typing import List

from ninja import Schema
from pydantic import validator, conint

from backend.xia.common.response.response_schema import ResponseModel
from backend.xia.enums.task.execute_target import ExecuteTargetType
from backend.xia.enums.task.state import StateType
from backend.xia.schemas.api_test.business import GetAllApiTestBusinesses
from backend.xia.schemas.api_test.project import GetAllApiTestProjects
from backend.xia.schemas.sys.crontab import GetAllCornTabs


class ApiTestTaskBase(Schema):
    name: str
    description: str = None
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    send_report: bool
    status: bool
    state: StateType = StateType.pause
    execute_target: ExecuteTargetType = ExecuteTargetType.case
    retry_num: conint(strict=True, ge=0, le=10)
    api_case: List[int] = None

    @validator('execute_target')
    def check_execute_target(cls, value):
        if value not in ExecuteTargetType.get_member_values():
            raise ValueError('执行目标参数错误')
        return value


class CreateApiTestTask(ApiTestTaskBase):
    sys_cron: int
    api_project: int
    api_business_test: int

    @validator('state')
    def check_state(cls, value):
        if value != StateType.pause:
            raise ValueError('任务运行状态参数错误，必须设置为暂停')
        return value


class UpdateApiTestTask(ApiTestTaskBase):
    sys_cron: int
    api_project: int
    api_business_test: int

    @validator('state')
    def check_state(cls, value):
        if value != StateType.pause:
            raise ValueError('任务运行状态参数错误，必须设置为暂停')
        return value


class GetAllApiTestTasks(ApiTestTaskBase):
    id: int
    sys_cron: GetAllCornTabs = None
    api_project: GetAllApiTestProjects = None
    api_business_test: GetAllApiTestBusinesses = None
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime

    @staticmethod
    def resolve_api_case(value):
        if value.api_case is not None:
            if len(value.api_case) > 0:
                return list(map(int, str(value.api_case).split(',')))
        return


class GetOneApiTestTaskResponse(ResponseModel):
    data: GetAllApiTestTasks = None
