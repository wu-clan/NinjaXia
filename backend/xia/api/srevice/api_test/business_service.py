#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.xia.common.exception import errors
from backend.xia.crud.api_test.business import ApiTestBusinessDao
from backend.xia.crud.api_test.case import ApiTestCaseDao
from backend.xia.crud.api_test.module import ApiTestModuleDao
from backend.xia.schemas.api_test.business import CreateApiTestBusiness, UpdateApiTestBusiness


def get_businesses():
    return ApiTestBusinessDao.get_all_businesses()


def get_business(pk: int):
    business = ApiTestBusinessDao.get_business_by_id(pk)
    if not business:
        raise errors.NotFoundError(msg='业务不存在')
    return ApiTestBusinessDao.get_one_business(pk)


def create(request, obj: CreateApiTestBusiness):
    if ApiTestBusinessDao.get_business_by_name(obj.name):
        raise errors.ForbiddenError(msg='业务已存在, 请更改模块名称')
    module = ApiTestModuleDao.get_module_by_id(obj.api_module)
    if not module:
        raise errors.NotFoundError(msg='模块不存在')
    if len(obj.api_cases) == 0:
        raise errors.ForbiddenError(msg='请选择用例')
    case_list = []
    for _case in set(obj.api_cases):
        case = ApiTestCaseDao.get_case_by_id(_case)
        if not case:
            raise errors.NotFoundError(msg=f'用例 {_case} 不存在')
        else:
            case_list.append(case)
    obj.api_module = module
    business, business_and_case = ApiTestBusinessDao.create_business(obj, case_list, request.session['user'])
    return business, business_and_case


def update(*, request, pk: int, obj: UpdateApiTestBusiness):
    business = ApiTestBusinessDao.get_business_by_id(pk)
    if not business:
        raise errors.NotFoundError(msg='业务不存在')
    if business.name != obj.name and ApiTestBusinessDao.get_business_by_name(obj.name):
        raise errors.ForbiddenError(msg='业务已存在, 请更改业务名称')
    module = ApiTestModuleDao.get_module_by_id(obj.api_module)
    if not module:
        raise errors.NotFoundError(msg='模块不存在')
    if len(obj.api_cases) == 0:
        raise errors.ForbiddenError(msg='请选择用例')
    case_list = []
    for _case in set(obj.api_cases):
        case = ApiTestCaseDao.get_case_by_id(_case)
        if not case:
            raise errors.NotFoundError(msg=f'用例 {_case} 不存在')
        else:
            case_list.append(case)
    obj.api_module = module
    count = ApiTestBusinessDao.update_business(pk, obj, case_list, request.session['user'])
    return count


def delete(pk: int):
    business = ApiTestBusinessDao.get_business_by_id(pk)
    if not business:
        raise errors.NotFoundError(msg='业务不存在')
    count = ApiTestBusinessDao.delete_business(pk)
    return count


def get_businesses_by_name(name: str):
    return ApiTestBusinessDao.get_all_businesses_by_name(name)


def get_cases_by_business(pk: int):
    return ApiTestBusinessDao.get_all_cases_by_business(pk)
