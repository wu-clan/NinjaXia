#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.crud.crud_sys.crud_sys_crontab import SysCrontabDao
from backend.schemas import Response404, Response200
from backend.schemas.sm_sys.sm_sys_crontab import GetAllCornTabs, CreateCornTab, UpdateCornTab
from backend.utils.serializers import serialize_data

v1_sys_crontab = Router()


@v1_sys_crontab.get('', summary='获取所有corn', response=List[GetAllCornTabs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_crontab(request):
    return SysCrontabDao.get_all_crontab()


@v1_sys_crontab.get('/{int:pk}', summary='获取单个corn', auth=GetCurrentUser())
def get_crontab(request, pk: int):
    corn = SysCrontabDao.get_crontab_by_id(pk)
    if not corn:
        return Response404(msg='定时任务不存在')
    return Response200(data=serialize_data(corn))


@v1_sys_crontab.post('', summary='创建corn', auth=GetCurrentIsSuperuser())
def create_crontab(request, obj: CreateCornTab):
    corn = SysCrontabDao.create_crontab(obj)
    corn.creator = request.session['username']
    corn.save()
    return Response200(data=serialize_data(corn))


@v1_sys_crontab.put('/{int:pk}', summary='更新corn', auth=GetCurrentIsSuperuser())
def update_crontab(request, pk: int, obj: UpdateCornTab):
    corn = SysCrontabDao.get_crontab_by_id(pk)
    if not corn:
        return Response404(msg='定时任务不存在')
    corn = SysCrontabDao.update_crontab(pk, obj)
    corn.modifier = request.session['username']
    corn.save()
    return Response200(data=serialize_data(corn))


@v1_sys_crontab.delete('/{int:pk}', summary='删除corn', auth=GetCurrentIsSuperuser())
def delete_crontab(request, pk: int):
    corn = SysCrontabDao.get_crontab_by_id(pk)
    if not corn:
        return Response404(msg='定时任务不存在')
    SysCrontabDao.delete_crontab(pk)
    return Response200()
