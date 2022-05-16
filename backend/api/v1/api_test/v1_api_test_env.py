#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_env import crud_api_test_env
from backend.schemas.v1.sm_api_test.sm_api_test_env import GetAllApiTestEnv

v1_api_test_env = Router()


@v1_api_test_env.get('/api_test_envs', summary='获取所有模块', response=List[GetAllApiTestEnv])
@paginate(CustomPagination)
def get_all_envs(request):
    return crud_api_test_env.get_all_envs()
