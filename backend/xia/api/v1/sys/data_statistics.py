#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

from backend.xia.common.response.response_schema import Response200
from backend.xia.crud.api_test.business import ApiTestBusinessDao
from backend.xia.crud.api_test.case import ApiTestCaseDao
from backend.xia.crud.api_test.env import ApiTestEnvDao
from backend.xia.crud.api_test.module import ApiTestModuleDao
from backend.xia.crud.api_test.project import ApiTestProjectDao
from backend.xia.crud.api_test.report import ApiTestReportDao, ApiTestReportDetailDao
from backend.xia.crud.api_test.task import ApiTestTaskDao

v1_sys_data_statistics = Router()


@v1_sys_data_statistics.get('', summary='获取系统数据统计信息')
def get_all_cases_data(request):
    api_projects = ApiTestProjectDao.get_project_count()
    api_modules = ApiTestModuleDao.get_module_count()
    api_envs = ApiTestEnvDao.get_env_count()
    api_businesses = ApiTestBusinessDao.get_business_count()
    api_cases = ApiTestCaseDao.get_case_count()
    api_tasks = ApiTestTaskDao.get_task_count()
    api_task_runs = ApiTestReportDao.get_report_count()
    api_test_case_reports = ApiTestReportDetailDao.get_report_detail_count()

    api_data_list = {
        'api_projects': api_projects,
        'api_modules': api_modules,
        'api_envs': api_envs,
        'api_businesses': api_businesses,
        'api_cases': api_cases,
        'api_tasks': api_tasks,
        'api_task_runs': api_task_runs,
        'api_test_case_reports': api_test_case_reports
    }

    return Response200(data={'api_data': api_data_list})
