#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.http import Http404
from ninja import Router
from ninja.pagination import paginate

from backend.common.log import log
from backend.ninja_models.models.api_auto.case import CaseCRUD
from backend.schemas import Message
from backend.schemas.case import CaseBase, CreateCase, GetCase

case = Router()


@case.post('/case', summary='添加测试用例', response=Message)
def create_case(request, post: CaseBase, ifc: CreateCase):
    if not CaseCRUD.get_case_by_name(post.name):
        try:
            CaseCRUD.get_interface_for_case(ifc.id)
        except Http404:
            log.error(f'The interface group {post.name} does not exist, please add the interface group first')
            return dict(code=403, msg='接口组不存在，请先添加接口组')
        CaseCRUD.create_case(post, ifc.id)
        log.success('successfully added use case')
        return dict(code=200, msg='添加用例成功', data=post)
    log.error('The use case already exists, please change the name of the use case and resubmit')
    return dict(code=403, msg='用例已存在，请更该用例名称后重新提交')


@case.put('/case', summary='更新测试用例', response=Message)
def update_case(request, ):
    pass


@case.delete('/case', summary='删除测试用例', response=Message)
def delete_case(request, ):
    pass


@case.get('/case', summary='获取所有测试用例', response=List[GetCase])
@paginate
def get_case(request, **kwargs):
    _cases = CaseCRUD.get_all_cases()
    log.success('get all cases successful')
    return _cases
