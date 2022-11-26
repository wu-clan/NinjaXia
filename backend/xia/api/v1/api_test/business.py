#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router, Query
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.api.srevice.api_test import business_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.api_test.business import CreateApiTestBusiness, \
    UpdateApiTestBusiness, GetOneBusinessesAndCasesResponse, GetAllApiTestBusinesses, GetAllApiTestBusinessesAndCases

v1_api_test_business = Router()


@v1_api_test_business.get('', summary='获取所有业务', response=List[GetAllApiTestBusinesses],
                          auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_businesses(request):
    return business_service.get_businesses()


@v1_api_test_business.get('/{int:pk}', summary='获取单个业务', response=GetOneBusinessesAndCasesResponse,
                          auth=GetCurrentUser())
def get_one_business(request, pk: int):
    business = business_service.get_business(pk)
    return GetOneBusinessesAndCasesResponse(data=business)


@v1_api_test_business.post('', summary='新增业务', auth=GetCurrentIsSuperuser())
def create_business(request, obj: CreateApiTestBusiness):
    business_service.create(request, obj)
    return response_base.response_200()


@v1_api_test_business.put('/{int:pk}', summary='更新业务', auth=GetCurrentIsSuperuser())
def update_business(request, pk: int, obj: UpdateApiTestBusiness):
    count = business_service.update(request=request, pk=pk, obj=obj)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_business.delete('/{int:pk}', summary='删除业务', auth=GetCurrentIsSuperuser())
def delete_business(request, pk: int):
    count = business_service.delete(pk)
    if count > 0:
        return response_base.response_200()
    return response_base.fail()


@v1_api_test_business.get('/name', summary='业务名称模糊匹配', auth=GetCurrentUser(),
                          response=List[GetAllApiTestBusinesses])
@paginate(CustomPagination)
def get_all_businesses_by_name(request, name: str = Query(...)):
    return business_service.get_businesses_by_name(name)


@v1_api_test_business.get('/{pk}/cases', summary='获取业务下所有测试用例',
                          response=List[GetAllApiTestBusinessesAndCases], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_cases_by_business(request, pk: int):
    return business_service.get_cases_by_business(pk)
