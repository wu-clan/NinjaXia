#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_business import crud_api_test_business
from backend.schemas.v1.sm_api_test.sm_api_test_business import GetAllApiTestBusiness

v1_api_test_business = Router()


@v1_api_test_business.get('', summary='获取所有模块', response=List[GetAllApiTestBusiness])
@paginate(CustomPagination)
def get_all_businesses(request):
    return crud_api_test_business.get_all_businesses()
