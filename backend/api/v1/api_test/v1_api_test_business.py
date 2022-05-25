#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.api.jwt_security import GetCurrentIsSuperuser, GetCurrentUser
from backend.common.pagination import CustomPagination
from backend.crud.crud_api_test.crud_api_test_business import crud_api_test_business
from backend.crud.crud_api_test.crud_api_test_case import crud_api_test_case
from backend.crud.crud_api_test.crud_api_test_module import crud_api_test_module
from backend.schemas import Response404, Response200, Response403
from backend.schemas.sm_api_test.sm_api_test_business import GetAllApiTestBusinesses, CreateApiTestBusiness, \
    GetAllApiTestBusinessesAndCases
from backend.utils.serializers import serialize_data

v1_api_test_business = Router()


@v1_api_test_business.get('', summary='获取所有业务', response=List[GetAllApiTestBusinessesAndCases], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_businesses(request):
    return crud_api_test_business.get_all_businesses()


@v1_api_test_business.get('/{int:pk}/cases', summary='获取指定业务下的用例', auth=GetCurrentUser())
def get_all_cases_by_business_id(request, pk: int):
    business = crud_api_test_business.get_business_by_id(pk)
    if not business:
        return Response404(msg='业务不存在')
    cases_list = crud_api_test_business.get_all_cases_by_business_id(pk)
    cases_info = []
    for case in cases_list:
        cases = serialize_data(case)
        cases_info.append(cases)
    return Response200(data={'cases': cases_info})


@v1_api_test_business.post('', summary='新增业务', auth=GetCurrentIsSuperuser())
def create_business(request, obj: CreateApiTestBusiness):
    if crud_api_test_business.get_business_by_name(obj.name):
        return Response403(msg='业务已存在, 请更改模块名称')
    module = crud_api_test_module.get_module_by_id(obj.api_module)
    if not module:
        return Response404(msg='模块不存在')
    if len(obj.api_cases) == 0:
        return Response403(msg='请选择用例')
    case_list = []
    for _case in obj.api_cases:
        case = crud_api_test_case.get_case_by_id(_case)
        if not case:
            return Response404(msg=f'用例 {_case} 不存在')
        else:
            case_list.append(case)
    obj.api_module = module
    _business, _business_and_case = crud_api_test_business.create_business(obj, case_list)
    # 更新创建者
    _business.creator = request.session['username']
    _business.save()
    for _bc in _business_and_case:
        _bc.creator = request.session['username']
        _bc.save()
    # 序列化
    business = serialize_data(_business)
    cases = []
    for bc in _business_and_case:
        cases.append(serialize_data(bc.api_case))
    return Response200(data={'business': business, 'cases': cases})


@v1_api_test_business.put('/{int:pk}', summary='更新业务', auth=GetCurrentIsSuperuser())
def update_business(request, pk: int, obj: CreateApiTestBusiness):
    business = crud_api_test_business.get_business_by_id(pk)
    if not business:
        return Response404(msg='业务不存在')
    if business.name != obj.name and crud_api_test_business.get_business_by_name(obj.name):
        return Response403(msg='业务已存在, 请更改业务名称')
    module = crud_api_test_module.get_module_by_id(obj.api_module)
    if not module:
        return Response404(msg='模块不存在')
    if len(obj.api_cases) == 0:
        return Response403(msg='请选择用例')
    case_list = []
    for _case in obj.api_cases:
        case = crud_api_test_case.get_case_by_id(_case)
        if not case:
            return Response404(msg=f'用例 {_case} 不存在')
        else:
            case_list.append(case)
    obj.api_module = module
    _business, _business_and_case = crud_api_test_business.update_business(pk, obj, case_list)
    _business.modifier = request.session['username']
    _business.save()
    for _bc in _business_and_case:
        _bc.creator = request.session['username']
        _bc.modifier = request.session['username']
        _bc.save()
    # 序列化
    business = serialize_data(_business)
    cases = []
    for bc in _business_and_case:
        cases.append(serialize_data(bc.api_case))
    return Response200(data={'business': business, 'cases': cases})


@v1_api_test_business.delete('/{int:pk}', summary='删除业务', auth=GetCurrentIsSuperuser())
def delete_business(request, pk: int):
    business = crud_api_test_business.get_business_by_id(pk)
    if not business:
        return Response404(msg='业务不存在')
    crud_api_test_business.delete_business(pk)
    return Response200()


@v1_api_test_business.get('/{str:name}', summary='业务名称模糊匹配', auth=GetCurrentUser(),
                          response=List[GetAllApiTestBusinesses])
@paginate(CustomPagination)
def get_all_businesses_by_name(request, name: str):
    return crud_api_test_business.get_all_businesses_by_name(name)
