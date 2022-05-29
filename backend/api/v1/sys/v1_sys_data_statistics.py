#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

from backend.api.jwt_security import GetCurrentUser
from backend.crud.crud_api_test.crud_api_test_business import crud_api_test_business
from backend.crud.crud_api_test.crud_api_test_case import crud_api_test_case
from backend.crud.crud_api_test.crud_api_test_env import crud_api_test_env
from backend.crud.crud_api_test.crud_api_test_module import crud_api_test_module
from backend.crud.crud_api_test.crud_api_test_project import crud_api_test_project
from backend.crud.crud_api_test.crud_api_test_report import crud_api_test_report, crud_api_test_report_detail
from backend.crud.crud_api_test.crud_api_test_task import crud_api_test_task
from backend.schemas import Response200

v1_sys_data_statistics = Router(auth=GetCurrentUser())


@v1_sys_data_statistics.get('', summary='获取系统数据统计信息')
def get_all_cases_data(request):
    api_projects = crud_api_test_project.get_project_count()
    api_modules = crud_api_test_module.get_module_count()
    api_envs = crud_api_test_env.get_env_count()
    api_businesses = crud_api_test_business.get_business_count()
    api_cases = crud_api_test_case.get_case_count()
    api_tasks = crud_api_test_task.get_task_count()
    api_task_runs = crud_api_test_report.get_report_count()
    api_test_case_reports = crud_api_test_report_detail.get_report_detail_count()

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
