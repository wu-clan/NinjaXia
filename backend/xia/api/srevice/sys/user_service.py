#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from email_validator import validate_email, EmailNotValidError

from backend.xia.api import jwt
from backend.xia.common.exception import errors
from backend.xia.crud.sys.user import UserDao
from backend.xia.schemas.sys.user import Login, CreateUser, UpdateUser


def login(obj: Login):
    current_user = UserDao.get_user_by_username(obj.username)
    if not current_user:
        raise errors.NotFoundError(msg='用户不存在')
    if not current_user.is_active:
        raise errors.AuthorizationError(msg='用户被锁定')
    if not authenticate(username=obj.username, password=obj.password):
        raise errors.AuthorizationError(msg='用户名或密码错误，请重试')
    UserDao.update_user_last_login(current_user)
    access_token = jwt.create_access_token(current_user.pk)
    return access_token, current_user.is_superuser


def register(obj: CreateUser):
    if UserDao.get_user_by_username(obj.username):
        raise errors.ForbiddenError(msg='用户名已注册，请修改后重新提交')
    if UserDao.get_user_by_email(email=obj.email):
        raise errors.ForbiddenError(msg='邮箱已注册，请修改后重新提交')
    try:
        validate_email(obj.email, check_deliverability=False).email
    except EmailNotValidError:
        raise errors.ForbiddenError(msg='电子邮件格式错误，请重新输入')
    UserDao.create_user(obj)


def update(*, request, username: str, obj: UpdateUser):
    if not request.auth.is_superuser:
        if not username == request.auth.username:
            raise errors.AuthorizationError
    input_user = UserDao.get_user_by_username(username)
    if not input_user:
        raise errors.NotFoundError(msg='用户不存在')
    if obj.username != input_user.username:
        if UserDao.get_user_by_username(obj.username):
            raise errors.ForbiddenError(msg='用户名已注册，请修改后重新提交')
    if obj.email != input_user.email:
        if UserDao.get_user_by_email(obj.email):
            raise errors.ForbiddenError(msg='邮箱已注册，请修改后重新提交')
    try:
        validate_email(obj.email, check_deliverability=False).email
    except EmailNotValidError:
        raise errors.ForbiddenError(msg='电子邮件格式错误，请重新输入')
    count = UserDao.update_user(input_user.pk, obj)
    return count


def get_user_info(username: str):
    user = UserDao.get_user_by_username(username)
    if not user:
        raise errors.NotFoundError(msg='用户不存在')
    return user


def get_user_list():
    user_list = UserDao.get_all_users()
    return user_list
