#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Schema


class ApiTestTaskBase(Schema):
    ...


class CreateApiTestTask(ApiTestTaskBase):
    ...


class UpdateApiTestTask(ApiTestTaskBase):
    ...


class GetAllApiTestTasks(ApiTestTaskBase):
    ...
