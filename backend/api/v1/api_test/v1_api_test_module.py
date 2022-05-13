#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_module import crud_api_test_module
from backend.schemas.v1.sm_api_test.sm_api_test_module import GetAllApiTestModules

v1_api_test_module = Router()


@v1_api_test_module.get('/all', summary='获取所有模块', response=List[GetAllApiTestModules])
@paginate(CustomPagination)
def get_all_modules(request):
    return crud_api_test_module.get_all_modules()
