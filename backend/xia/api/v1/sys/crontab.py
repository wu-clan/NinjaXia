#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.sys import crontab_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.sys.crontab import GetAllCornTabs, CreateCornTab, UpdateCornTab

v1_sys_crontab = Router()


@v1_sys_crontab.get('', summary='获取所有cron', response=List[GetAllCornTabs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_crontabs(request):
    return crontab_service.get_all_crontabs()


@v1_sys_crontab.get('/{pk}', summary='获取单个cron', auth=GetCurrentUser())
def get_crontab(request, pk: int):
    cron = crontab_service.get_crontab(pk)
    return response_base.response_200(data=cron, exclude={'_state'})


@v1_sys_crontab.post('', summary='创建cron', auth=GetCurrentIsSuperuser())
def create_crontab(request, obj: CreateCornTab):
    crontab_service.create(request=request, obj=obj)
    return response_base.response_200()


@v1_sys_crontab.put('/{pk}', summary='更新cron', auth=GetCurrentIsSuperuser())
def update_crontab(request, pk: int, obj: UpdateCornTab):
    count = crontab_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_sys_crontab.delete('/{pk}', summary='删除cron', auth=GetCurrentIsSuperuser())
def delete_crontab(request, pk: int):
    count = crontab_service.delete(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()
