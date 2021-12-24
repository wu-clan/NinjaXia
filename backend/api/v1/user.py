#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from ninja import Router
from ninja.responses import codes_4xx

from backend.schemas import Message, Token
from backend.schemas.user import Login

user = Router()


@user.post('/login', summary='登录', description='Auth 登录', response={200: Token, codes_4xx: Message})
def login(request, post: Login):
    current_user = User.objects.filter(username=post.username)
    if not current_user:
        return 404, {'msg': '用户不存在'}
    if not current_user.first().is_active:
        return 403, {'msg': '用户已被锁定'}
    if not authenticate(username=post.username, password=post.password):
        return 403, {'msg': '密码错误, 请重新输入'}
    return 200, {'result': '登陆成功', 'token': 'xxx'}
