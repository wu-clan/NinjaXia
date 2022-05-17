#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_case import crud_api_test_case
from backend.schemas.v1.sm_api_test.sm_api_test_case import GetAllApiTestCase

v1_api_test_case = Router()


@v1_api_test_case.get('', summary='获取所有模块', response=List[GetAllApiTestCase])
@paginate(CustomPagination)
def get_all_cases(request):
    return crud_api_test_case.get_all_cases()
