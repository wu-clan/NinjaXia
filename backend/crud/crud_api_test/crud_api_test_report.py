#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from django.db import transaction
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models.api_test.api_test_report import ApiTestReport, ApiTestReportDetail
from backend.schemas.sm_api_test.sm_api_test_report import CreateApiTestReport, UpdateApiTestReport


class CRUDApiTestTask(CRUDBase[ApiTestReport, CreateApiTestReport, UpdateApiTestReport]):

    def get_all_reports(self) -> QuerySet:
        return super().get_all().order_by('-modified_time')

    @transaction.atomic
    def create_report(self, data: dict) -> ApiTestReport:
        return self.model.objects.create(**data)


crud_api_test_report = CRUDApiTestTask(ApiTestReport)


class CRUDApiTestReportDetail(CRUDBase[ApiTestReportDetail, CreateApiTestReport, UpdateApiTestReport]):

    def get_all_reports_detail(self) -> QuerySet:
        report_list = super().get_all().order_by('-created_time')
        for report in report_list:
            report.params = json.loads(json.dumps(eval(report.params))) \
                if isinstance(report.params, str) else report.params
            report.headers = json.loads(json.dumps(eval(report.headers))) \
                if isinstance(report.headers, str) else report.params
            report.response_data = json.loads(json.dumps(eval(report.response_data))) \
                if isinstance(report.response_data, str) else report.params
        return report_list

    @transaction.atomic
    def create_report_detail(self, data: dict) -> ApiTestReportDetail:
        return self.model.objects.create(**data)

    @transaction.atomic
    def create_report_detail_list(self, data_list: list) -> list:
        return self.model.objects.bulk_create(data_list)


crud_api_test_report_detail = CRUDApiTestReportDetail(ApiTestReportDetail)
