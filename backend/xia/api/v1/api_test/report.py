#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.common.pagination import CustomPagination
from backend.xia.common.security.jwt_security import GetCurrentUser
from backend.xia.crud.api_test.report import ApiTestReportDao, ApiTestReportDetailDao
from backend.xia.schemas.api_test.report import GetAllApiTestReports, GetAllApiTestReportsDetail

v1_api_test_report = Router()


@v1_api_test_report.get('', summary='获取所有测试报告', response=List[GetAllApiTestReports], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports(request):
    return ApiTestReportDao.get_all_reports()


@v1_api_test_report.get('/detail', summary='获取所有测试报告详情', response=List[GetAllApiTestReportsDetail],
                        auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports_detail(request):
    return ApiTestReportDetailDao.get_all_reports_detail()


@v1_api_test_report.get('/{int:pk}/detail', summary='获取单个简约报告下所有测试报告详情',
                        response=List[GetAllApiTestReportsDetail], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports_detail_by_report_id(request, pk: int):
    return ApiTestReportDetailDao.get_all_reports_detail_by_report_id(pk)
