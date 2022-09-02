#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import Response404, Response403, Response200
from backend.xia.common.security.jwt_security import GetCurrentUser, GetCurrentIsSuperuser
from backend.xia.crud.api_test.business import ApiTestBusinessDao
from backend.xia.crud.api_test.case import ApiTestCaseDao
from backend.xia.crud.api_test.module import ApiTestModuleDao
from backend.xia.schemas.api_test.business import CreateApiTestBusiness, \
    GetAllApiTestBusinessesAndCases, BusinessesAndCasesResponse

v1_api_test_business = Router()


@v1_api_test_business.get('', summary='获取所有业务', response=List[GetAllApiTestBusinessesAndCases],
                          auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_businesses(request):
    return ApiTestBusinessDao.get_all_businesses()


@v1_api_test_business.get('/{int:pk}/cases', summary='获取单个业务', auth=GetCurrentUser())
def get_one_business(request, pk: int):
    business = ApiTestBusinessDao.get_business_by_id(pk)
    if not business:
        return Response404(msg='业务不存在')
    cases = ApiTestBusinessDao.get_one_business(pk)
    return BusinessesAndCasesResponse(data=list(cases))


@v1_api_test_business.post('', summary='新增业务', auth=GetCurrentIsSuperuser())
def create_business(request, obj: CreateApiTestBusiness):
    if ApiTestBusinessDao.get_business_by_name(obj.name):
        return Response403(msg='业务已存在, 请更改模块名称')
    module = ApiTestModuleDao.get_module_by_id(obj.api_module)
    if not module:
        return Response404(msg='模块不存在')
    if len(obj.api_cases) == 0:
        return Response403(msg='请选择用例')
    case_list = []
    for _case in set(obj.api_cases):
        case = ApiTestCaseDao.get_case_by_id(_case)
        if not case:
            return Response404(msg=f'用例 {_case} 不存在')
        else:
            case_list.append(case)
    obj.api_module = module
    business, business_and_case = ApiTestBusinessDao.create_business(obj, case_list)
    # 更新创建者
    business.creator = request.session['username']
    business.save()
    for bc in business_and_case:
        bc.creator = request.session['username']
        bc.save()
    return BusinessesAndCasesResponse(data=list(business_and_case))


@v1_api_test_business.put('/{int:pk}', summary='更新业务', auth=GetCurrentIsSuperuser())
def update_business(request, pk: int, obj: CreateApiTestBusiness):
    business = ApiTestBusinessDao.get_business_by_id(pk)
    if not business:
        return Response404(msg='业务不存在')
    if business.name != obj.name and ApiTestBusinessDao.get_business_by_name(obj.name):
        return Response403(msg='业务已存在, 请更改业务名称')
    module = ApiTestModuleDao.get_module_by_id(obj.api_module)
    if not module:
        return Response404(msg='模块不存在')
    if len(obj.api_cases) == 0:
        return Response403(msg='请选择用例')
    case_list = []
    for _case in set(obj.api_cases):
        case = ApiTestCaseDao.get_case_by_id(_case)
        if not case:
            return Response404(msg=f'用例 {_case} 不存在')
        else:
            case_list.append(case)
    obj.api_module = module
    business, business_and_case = ApiTestBusinessDao.update_business(pk, obj, case_list)
    business.modifier = request.session['username']
    business.save()
    for bc in business_and_case:
        bc.creator = request.session['username']
        bc.modifier = request.session['username']
        bc.save()
    return BusinessesAndCasesResponse(data=list(business_and_case))


@v1_api_test_business.delete('/{int:pk}', summary='删除业务', auth=GetCurrentIsSuperuser())
def delete_business(request, pk: int):
    business = ApiTestBusinessDao.get_business_by_id(pk)
    if not business:
        return Response404(msg='业务不存在')
    ApiTestBusinessDao.delete_business(pk)
    return Response200()


@v1_api_test_business.get('/{str:name}', summary='业务名称模糊匹配', auth=GetCurrentUser(),
                          response=List[GetAllApiTestBusinessesAndCases])
@paginate(CustomPagination)
def get_all_businesses_by_name(request, name: str):
    return ApiTestBusinessDao.get_all_businesses_by_name(name)
