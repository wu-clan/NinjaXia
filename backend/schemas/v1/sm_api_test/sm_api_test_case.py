#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Schema


class ApiTestCaseBase(Schema):
    ...


class CreateApiTestCase(ApiTestCaseBase):
    ...


class UpdateApiTestCase(ApiTestCaseBase):
    ...


class GetAllApiTestCase(ApiTestCaseBase):
    ...
