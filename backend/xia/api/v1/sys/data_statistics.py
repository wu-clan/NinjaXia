#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

from backend.xia.api.srevice.sys import data_statistics_service
from backend.xia.common.response.response_schema import response_base

v1_sys_data_statistics = Router()


@v1_sys_data_statistics.get('', summary='获取系统数据统计信息')
def get_all_resources_data(request):
    data = data_statistics_service.get_resource_count()
    return response_base.response_200(data=data)
