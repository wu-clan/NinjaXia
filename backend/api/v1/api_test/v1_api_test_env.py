#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentIsSuperuser, GetCurrentUser
from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_env import crud_api_test_env
from backend.schemas import Response404, Response200, Response403
from backend.schemas.sm_api_test.sm_api_test_case import GetAllApiTestCases
from backend.schemas.sm_api_test.sm_api_test_env import GetAllApiTestEnvs, CreateApiTestEnv
from backend.utils.serializers import serialize_data

v1_api_test_env = Router()


@v1_api_test_env.get('', summary='获取所有环境', response=List[GetAllApiTestEnvs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_envs(request):
    return crud_api_test_env.get_all_envs()


@v1_api_test_env.get('/enable', summary='获取所有已启用环境', response=List[GetAllApiTestEnvs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_enable_envs(request):
    return crud_api_test_env.get_all_enable_envs()


@v1_api_test_env.get('/{int:pk}', summary='获取单个环境', auth=GetCurrentUser())
def get_one_env(request, pk: int):
    env = crud_api_test_env.get_env_by_id(pk)
    if not env:
        return Response404(msg='环境不存在')
    return Response200(data=serialize_data(env))


@v1_api_test_env.post('', summary='新增环境', auth=GetCurrentIsSuperuser())
def create_env(request, obj: CreateApiTestEnv):
    env = crud_api_test_env.get_env_by_name(obj.name)
    if env:
        return Response403(msg='环境已存在, 请更换环境名称')
    new_env = crud_api_test_env.create_env(obj)
    new_env.creator = request.session['username']
    new_env.save()
    return Response200(data=serialize_data(new_env))


@v1_api_test_env.put('/{int:pk}', summary='更新环境', auth=GetCurrentIsSuperuser())
def update_env(request, pk: int, obj: CreateApiTestEnv):
    env = crud_api_test_env.get_env_by_id(pk)
    if not env:
        return Response404(msg='环境不存在')
    if not env.name == obj.name:
        if crud_api_test_env.get_env_by_name(obj.name):
            return Response403(msg='环境已存在, 请更换环境名称')
    new_env = crud_api_test_env.update_env(pk, obj)
    new_env.modifier = request.session['username']
    new_env.save()
    return Response200(data=serialize_data(new_env))


@v1_api_test_env.delete('/{int:pk}', summary='删除环境', auth=GetCurrentIsSuperuser())
def delete_env(request, pk: int):
    env = crud_api_test_env.get_env_by_id(pk)
    if not env:
        return Response404(msg='环境不存在')
    crud_api_test_env.delete_env(pk)
    return Response200()


@v1_api_test_env.get('/{int:pk}/cases', response=List[GetAllApiTestCases], summary='获取单个环境所有用例', auth=GetCurrentUser())
@paginate(CustomPagination)
def get_one_env_cases(request, pk: int):
    try:
        _env = crud_api_test_env.get_env_or_404(pk)
    except Http404:
        raise Http404('环境不存在')
    cases = crud_api_test_env.get_env_cases(pk)
    return cases
