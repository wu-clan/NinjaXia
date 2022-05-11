#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Optional

from django.contrib import auth
from django.contrib.auth.models import User
from jose import jwt
from ninja.security import HttpBearer
from pydantic import ValidationError

from backend.crud.crud_user import crud_user
from backend.ninja_xia import settings
from backend.schemas import TokenError, AuthorizationError


def create_access_token(data: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    生成加密 token
    :param data: 登录提供的数据
    :param expires_delta: 设置到期时间
    :return: 加密token
    """
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(settings.TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.TOKEN_ALGORITHM)
    return encoded_jwt


class GetCurrentUser(HttpBearer):

    def authenticate(self, request, token) -> User:
        """
        验证当前用户并返回
        :param request:
        :param token:
        :return:
        """
        try:
            # 解密token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
            user_id = payload.get('sub')
            if not user_id:
                raise TokenError
        except (jwt.JWTError, ValidationError):
            raise TokenError
        user = crud_user.get_user_by_id(user_id)
        # 将用户登录信息存入session
        # auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return user


class GetCurrentIsSuperuser(GetCurrentUser):

    def authenticate(self, request, token) -> User:
        """
        验证当前超级用户并返回
        :param request:
        :param token:
        :return:
        """
        user = super().authenticate(request, token)
        if not user.is_superuser:
            raise AuthorizationError
        return user
