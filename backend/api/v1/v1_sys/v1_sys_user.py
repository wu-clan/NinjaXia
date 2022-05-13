#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Any

import orjson
from django.contrib.auth import authenticate
from django.core import serializers
from email_validator import validate_email, EmailNotValidError
from ninja import Router
from ninja.pagination import paginate

from backend.api.security import create_access_token, GetCurrentUser, GetCurrentIsSuperuser
from backend.common.pagination import CustomPagination
from backend.crud.crud_sys.crud_sys_user import crud_user
from backend.schemas import Response200, Response404, Response403
from backend.schemas.sm_api_test.sm_api_test_token import Token
from backend.schemas.sm_sys.sm_sys_user import CreateUser, Login, GetUsers, UpdateUser

user = Router()


@user.post('/login', summary='登录', description='Auth登录')
def login(request, obj: Login) -> Any:
    current_user = crud_user.get_user_by_username(obj.username)
    if not current_user:
        return Response404()
    if not current_user.is_active:
        return Response403(msg='用户被锁定')
    if not authenticate(username=obj.username, password=obj.password):
        return Response403(msg='用户名或密码错误，请重试')
    crud_user.update_user_last_login(current_user)
    access_token = create_access_token(current_user.pk)
    return Token(
        msg='success',
        access_token=access_token,
        token_type='bearer',
        is_superuser=current_user.is_superuser,
    )


@user.post('/register', summary='用户注册')
def register(request, obj: CreateUser):
    if crud_user.get_user_by_username(obj.username):
        return Response403(msg='用户名已注册，请修改后重新提交')
    if crud_user.get_user_by_email(email=obj.email):
        return Response403(msg='邮箱已注册，请修改后重新提交')
    try:
        validate_email(obj.email).email
    except EmailNotValidError:
        return Response403(msg='电子邮件格式错误，请重新输入')
    crud_user.create_user(obj)
    return Response200(data={
        'username': obj.username,
        'email': obj.emial
    })


@user.put('/users', summary='更新用户信息', auth=GetCurrentUser())
def update_user(request, obj: UpdateUser):
    current_user = request.auth
    if obj.username != current_user.username:
        if crud_user.get_user_by_username(obj.username):
            return Response403(msg='用户名已注册，请修改后重新提交')
    if obj.email != current_user.email:
        if crud_user.get_user_by_email(obj.email):
            return Response403(msg='邮箱已注册，请修改后重新提交')
    try:
        validate_email(obj.email).email
    except EmailNotValidError:
        return Response403(msg='电子邮件格式错误，请重新输入')
    crud_user.put_user(current_user.pk, obj)
    return Response200(data=obj)


@user.post('/logout', summary='用户退出', auth=GetCurrentUser())
def logout(request):
    return Response200()


@user.get('/userinfo', summary='获取用户信息', auth=GetCurrentUser())
def get_user_info(request):
    data = orjson.loads(serializers.serialize('json', [request.auth]))[0]
    return Response200(data=data)


@user.get('/users', summary='获取所有用户信息', auth=GetCurrentIsSuperuser(), response=List[GetUsers])
@paginate(CustomPagination)
def get_users(request):
    return crud_user.get_all_users()
