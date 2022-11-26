#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from backend.xia.common.exception import errors
from backend.xia.crud.api_test.report import ApiTestReportDao, ApiTestReportDetailDao


def get_all_reports():
    return ApiTestReportDao.get_all_reports()


def get_all_reports_detail():
    return ApiTestReportDetailDao.get_all_reports_detail()


def get_report_all_details(pk: int):
    return ApiTestReportDetailDao.get_all_reports_detail_by_report_id(pk)


def delete(pk: List[int]):
    for i in pk:
        case = ApiTestReportDetailDao.get_report_by_id(i)
        if not case:
            raise errors.NotFoundError(msg=f'测试报告 {i} 不存在')
    count = ApiTestReportDetailDao.delete_reports(pk)
    return count
