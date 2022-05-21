#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Schema


class ApiTestReportBase(Schema):
    ...


class CreateApiTestReport(ApiTestReportBase):
    ...


class UpdateApiTestReport(ApiTestReportBase):
    ...


class GetAllApiTestReports(ApiTestReportBase):
    ...
