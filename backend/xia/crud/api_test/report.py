#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import QuerySet

from backend.xia.crud.base import CRUDBase
from backend.xia.models.api_test.report import ApiTestReport, ApiTestReportDetail
from backend.xia.schemas.api_test.report import CreateApiTestReport, UpdateApiTestReport, CreateApiTestReportDetail, \
    UpdateApiTestReportDetail


class CRUDApiTestTask(CRUDBase[ApiTestReport, CreateApiTestReport, UpdateApiTestReport]):

    def get_all_reports(self) -> QuerySet:
        return super().get_all().order_by('-updated_time')

    @transaction.atomic
    def create_report(self, data: dict) -> ApiTestReport:
        return self.model.objects.create(**data)

    def get_report_count(self) -> int:
        return super().get_all().count()


ApiTestReportDao = CRUDApiTestTask(ApiTestReport)


class CRUDApiTestReportDetail(CRUDBase[ApiTestReportDetail, CreateApiTestReportDetail, UpdateApiTestReportDetail]):

    def get_all_reports_detail(self) -> QuerySet:
        return super().get_all().order_by('-id')

    @transaction.atomic
    def create_report_detail(self, data: dict) -> ApiTestReportDetail:
        return self.model.objects.create(**data)

    @transaction.atomic
    def create_report_detail_list(self, data_list: list) -> list:
        return self.model.objects.bulk_create(data_list)

    def get_report_detail_count(self) -> int:
        return super().get_all().count()

    def get_all_reports_detail_by_report_id(self, pk: int) -> QuerySet:
        return self.model.objects.filter(api_report=pk).all().order_by('-id')

    def get_report_by_id(self, pk: int):
        return super().get(pk)

    @transaction.atomic
    def delete_reports(self, pk: list) -> int:
        return self.model.objects.filter(id__in=pk).delete()[0]


ApiTestReportDetailDao = CRUDApiTestReportDetail(ApiTestReportDetail)
