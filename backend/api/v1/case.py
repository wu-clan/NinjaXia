#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.http import Http404
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from backend.common.log import log
from backend.ninja_models.models.api_auto.case import CaseCRUD
from backend.schemas import Message
from backend.schemas.case import CaseBase, CreateCase, GetCase, UpdateCase

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


@case.put('/case/{cid}', summary='更新测试用例', response=Message)
def update_case(request, cid: int, put: CaseBase, iid: UpdateCase):
    try:
        _case = CaseCRUD.get_case_by_id(cid)
    except Http404:
        log.error('use case does not exist please re enter')
        raise HttpError(404, '用例不存在，请重新输输入')
    if not CaseCRUD.get_case_name_by_id(cid) == put.name:
        if CaseCRUD.get_case_by_name(put.name):
            log.error(f'Use case name {put.name} already exists, please change and resubmit')
            return dict(code=403, msg='用例名已存在，请更改后重新提交')
    try:
        CaseCRUD.get_interface_for_case(iid.id)
    except Http404:
        log.error('The interface group does not exist, please re-enter')
        raise HttpError(404, '接口组不存在，请重新输入')
    for attr, value in put.dict().items():
        setattr(_case, attr, value)
    _case.interface_id = iid.id
    _case.save()
    log.success(f'successfully updated the use case {_case.id}:{_case.name}')
    return dict(code=200, msg='更新用例成功', data=put)


@case.delete('/case/{cid}', summary='删除测试用例', response=Message)
def delete_case(request, cid: int):
    try:
        _case = CaseCRUD.get_case_by_id(cid)
        _name = CaseCRUD.get_case_name_by_id(cid)
    except Http404:
        log.error('use case does not exist please re enter')
        raise HttpError(404, '用例不存在，请重新输输入')
    _case.delete()
    log.success(f'use case {_name} deleted successfully')
    return dict(code=200, msg='删除用例成功')


@case.get('/case', summary='获取所有测试用例', response=List[GetCase])
@paginate
def get_case(request, **kwargs):
    _cases = CaseCRUD.get_all_cases()
    log.success('get all cases successful')
    return _cases


@case.get('/case/{cid}', summary='获取单个测试用例', response=GetCase)
def get_case(request, cid: int):
    _case = CaseCRUD.get_case_by_id(cid)
    log.success('get one case successful')
    return _case
