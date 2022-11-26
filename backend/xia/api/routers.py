#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

from backend.xia.api.v1.api_test.business import v1_api_test_business
from backend.xia.api.v1.api_test.case import v1_api_test_case
from backend.xia.api.v1.api_test.env import v1_api_test_env
from backend.xia.api.v1.api_test.module import v1_api_test_module
from backend.xia.api.v1.api_test.project import v1_api_test_project
from backend.xia.api.v1.api_test.report import v1_api_test_report
from backend.xia.api.v1.api_test.task import v1_api_test_task
from backend.xia.api.v1.sys.crontab import v1_sys_crontab
from backend.xia.api.v1.sys.data_statistics import v1_sys_data_statistics
from backend.xia.api.v1.sys.email import v1_sys_email
from backend.xia.api.v1.sys.task import v1_sys_task
from backend.xia.api.v1.sys.user import v1_sys_user

v1 = Router()

v1.add_router('/sys_data_statistics', v1_sys_data_statistics, tags=['v1_数据统计'])

v1.add_router('/sys_users', v1_sys_user, tags=['v1_系统用户'])

v1.add_router('/sys_emails', v1_sys_email, tags=['v1_系统邮件管理'])

v1.add_router('/api_test_projects', v1_api_test_project, tags=['v1_api_项目管理'])

v1.add_router('/api_test_modules', v1_api_test_module, tags=['v1_api_模块管理'])

v1.add_router('/api_test_envs', v1_api_test_env, tags=['v1_api_环境管理'])

v1.add_router('/api_test_cases', v1_api_test_case, tags=['v1_api_用例管理'])

v1.add_router('/api_test_businesses', v1_api_test_business, tags=['v1_api_业务管理'])

v1.add_router('/sys_crontabs', v1_sys_crontab, tags=['v1_系统Crontab管理'])

v1.add_router('/api_test_tasks', v1_api_test_task, tags=['v1_api_任务管理'])

v1.add_router('/sys_tasks', v1_sys_task, tags=['v1_系统任务管理'])

v1.add_router('/api_test_reports', v1_api_test_report, tags=['v1_api_报告管理'])
