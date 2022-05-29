#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser
from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_report import crud_api_test_report, crud_api_test_report_detail
from backend.schemas.sm_api_test.sm_api_test_report import GetAllApiTestReports, GetAllApiTestReportsDetail

v1_api_test_report = Router()


@v1_api_test_report.get('', summary='获取所有测试报告', response=List[GetAllApiTestReports], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports(request):
    return crud_api_test_report.get_all_reports()


@v1_api_test_report.get('/detail', summary='获取所有测试报告详情', response=List[GetAllApiTestReportsDetail],
                        auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports_detail(request):
    return crud_api_test_report_detail.get_all_reports_detail()
