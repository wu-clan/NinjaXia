#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_report import crud_api_test_report
from backend.schemas.v1.sm_api_test.sm_api_test_report import GetAllApiTestReports

v1_api_test_report = Router()


@v1_api_test_report.get('/all', summary='获取所有模块', response=List[GetAllApiTestReports])
@paginate(CustomPagination)
def get_all_reports(request):
    return crud_api_test_report.get_all_reports()
