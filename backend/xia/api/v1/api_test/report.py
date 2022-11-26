#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.srevice.api_test import report_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.api_test.report import GetAllApiTestReports, GetAllApiTestReportsDetail

v1_api_test_report = Router()


@v1_api_test_report.get('', summary='获取所有测试报告', response=List[GetAllApiTestReports], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports(request):
    return report_service.get_all_reports()


@v1_api_test_report.get('/detail', summary='获取所有测试报告详情', response=List[GetAllApiTestReportsDetail],
                        auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports_detail(request):
    return report_service.get_all_reports_detail()


@v1_api_test_report.get('/{int:pk}/detail', summary='获取单个简约报告下所有测试报告详情',
                        response=List[GetAllApiTestReportsDetail], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_reports_detail_by_report_id(request, pk: int):
    return report_service.get_report_all_details(pk)


@v1_api_test_report.delete('', summary='批量删除测试用例', auth=GetCurrentIsSuperuser())
def delete_reports_detail(request, pk: List[int]):
    count = report_service.delete(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()
