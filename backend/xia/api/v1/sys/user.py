#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

from ninja import Router
from ninja.pagination import paginate

from backend.xia.api.jwt import GetCurrentUser
from backend.xia.api.srevice.sys import user_service
from backend.xia.common.pagination import CustomPagination
from backend.xia.common.response.response_schema import response_base
from backend.xia.schemas.sys.token import Token
from backend.xia.schemas.sys.user import CreateUser, Login, GetAllUsers, UpdateUser

v1_sys_user = Router()


@v1_sys_user.post('/login', summary='登录', response=Token)
def login(request, obj: Login) -> Any:
    access_token, is_superuser = user_service.login(obj)
    return Token(access_token=access_token, is_superuser=is_superuser)


@v1_sys_user.post('/register', summary='用户注册')
def register(request, obj: CreateUser):
    user_service.register(obj)
    return response_base.response_200(msg='用户注册成功')


@v1_sys_user.post('/logout', summary='用户退出', auth=GetCurrentUser())
def logout(request):
    return response_base.response_200(msg='退出登陆成功')


@v1_sys_user.put('/{username}', summary='更新用户信息', auth=GetCurrentUser())
def update_user(request, username: str, obj: UpdateUser):
    count = user_service.update(request=request, username=username, obj=obj)
    if count > 0:
        return response_base.response_200(msg='更新用户信息成功')
    return response_base.fail()


@v1_sys_user.get('/{username}', summary='获取用户信息', auth=GetCurrentUser())
def get_user_info(request, username: str):
    user = user_service.get_user_info(username)
    return response_base.response_200(data=user, exclude={'_state', 'password'})


@v1_sys_user.get('', summary='获取所有用户信息', response=List[GetAllUsers], auth=GetCurrentUser())
@paginate(CustomPagination)
def get_all_users(request):
    return user_service.get_user_list()
