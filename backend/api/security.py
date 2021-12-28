#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from ninja.security import HttpBearer

from backend.autoproject import settings


class AuthBearer(HttpBearer):
    """临时官方方案"""
    def authenticate(self, request, token):
        if token == "1":
            return token


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
        expires = datetime.utcnow() + timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expires, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

