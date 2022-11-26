#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.api_test import env_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.api_test.case import GetAllApiTestCases
from backend.xia.schemas.api_test.env import GetAllApiTestEnvs, CreateApiTestEnv, UpdateApiTestEnv

v1_api_test_env = Router()


@v1_api_test_env.get('', summary='获取所有环境', response=List[GetAllApiTestEnvs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_envs(request):
    return env_service.get_envs()


@v1_api_test_env.get('/enable', summary='获取所有已启用环境', response=List[GetAllApiTestEnvs], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_enable_envs(request):
    return env_service.get_open_envs()


@v1_api_test_env.get('/{int:pk}', summary='获取单个环境', auth=GetCurrentUser())
def get_one_env(request, pk: int):
    env = env_service.get_env(pk)
    return response_base.response_200(data=env, exclude={'_state'})


@v1_api_test_env.post('', summary='新增环境', auth=GetCurrentIsSuperuser())
def create_env(request, obj: CreateApiTestEnv):
    env_service.create(request=request, obj=obj)
    return response_base.response_200()


@v1_api_test_env.put('/{int:pk}', summary='更新环境', auth=GetCurrentIsSuperuser())
def update_env(request, pk: int, obj: UpdateApiTestEnv):
    count = env_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_env.delete('/{int:pk}', summary='删除环境', auth=GetCurrentIsSuperuser())
def delete_env(request, pk: int):
    count = env_service.delete(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_env.get('/{int:pk}/cases', response=List[GetAllApiTestCases], summary='获取单个环境所有用例',
                     auth=GetCurrentUser())
@paginate(CustomPagination)
def get_one_env_cases(request, pk: int):
    return env_service.get_env_cases(pk)
