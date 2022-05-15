#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.db.models import QuerySet

from backend.crud.base import CRUDBase
from backend.ninja_models.models.v1.api_test.api_test_report import ApiTestReport
from backend.schemas.v1.sm_api_test.sm_api_test_report import CreateApiTestReport, UpdateApiTestReport


class CRUDApiTestTask(CRUDBase[ApiTestReport, CreateApiTestReport, UpdateApiTestReport]):

    def get_all_reports(self) -> QuerySet:
        return super().get_all()


crud_api_test_report = CRUDApiTestTask(ApiTestReport)