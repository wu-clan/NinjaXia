#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.crud.crud_sys.crud_sys_crontab import crud_crontab
from backend.schemas import Response404, Response200
from backend.schemas.sm_sys.sm_sys_crontab import GetAllCornTabs, CreateCornTab, UpdateCornTab
from backend.utils.serializers import serialize_data

v1_sys_crontab = Router()


@v1_sys_crontab.get('', summary='获取所有定时任务', response=List[GetAllCornTabs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_crontab(request):
    return crud_crontab.get_all_crontab()


@v1_sys_crontab.get('/{int:pk}', summary='获取单个定时任务', auth=GetCurrentUser())
def get_crontab(request, pk: int):
    corn = crud_crontab.get_crontab_by_id(pk)
    if not corn:
        return Response404(msg='定时任务不存在')
    return Response200(data=serialize_data(corn))


@v1_sys_crontab.post('', summary='创建定时任务', auth=GetCurrentIsSuperuser())
def create_crontab(request, obj: CreateCornTab):
    corn = crud_crontab.create_crontab(obj)
    corn.creator = request.session['username']
    corn.save()
    return Response200(data=serialize_data(corn))


@v1_sys_crontab.put('/{int:pk}', summary='更新定时任务', auth=GetCurrentIsSuperuser())
def update_crontab(request, pk: int, obj: UpdateCornTab):
    corn = crud_crontab.get_crontab_by_id(pk)
    if not corn:
        return Response404(msg='定时任务不存在')
    corn = crud_crontab.update_crontab(pk, obj)
    corn.modifier = request.session['username']
    corn.save()
    return Response200(data=serialize_data(corn))


@v1_sys_crontab.delete('/{int:pk}', summary='删除定时任务', auth=GetCurrentIsSuperuser())
def delete_crontab(request, pk: int):
    corn = crud_crontab.get_crontab_by_id(pk)
    if not corn:
        return Response404(msg='定时任务不存在')
    crud_crontab.delete_crontab(pk)
    return Response200()
