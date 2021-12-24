#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from email_validator import EmailNotValidError, validate_email
from ninja import Router
from ninja.errors import HttpError
from ninja.responses import codes_4xx

from backend.schemas import Message, Token
from backend.schemas.user import CreateUser, Login

user = Router()


@user.post('/login', summary='登录', description='Auth 登录', response={200: Token, codes_4xx: Message})
def login(request, post: Login):
    current_user = User.objects.filter(username=post.username)
    if not current_user:
        return 404, dict(code=404, msg='用户不存在')
    if not current_user.first().is_active:
        return 403, dict(code=403, msg='用户已被锁定')
    if not authenticate(username=post.username, password=post.password):
        return 403, dict(msg='密码错误, 请重新输入')
    return 200, dict(result='登陆成功', token='xxx')


@user.post('/register', summary='用户注册', response={200: Message, codes_4xx: Message})
def register(request, post: CreateUser):
    if User.objects.filter(username=post.username):
        return 403, dict(code=403, msg='用户名已被注册,请修改后重新提交')
    if User.objects.filter(email=post.email):
        return 403, dict(code=403, msg='邮箱已被注册,请修改后重新提交')
    try:
        validate_email(post.email).email
    except EmailNotValidError:
        raise HttpError(403, '邮箱格式错误,情重新输入')
    User.objects.create_user(**post.dict())
    return dict(code=200, msg='注册成功', data=dict(username=post.username, email=post.email))

