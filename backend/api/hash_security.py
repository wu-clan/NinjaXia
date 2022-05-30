#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from passlib.context import CryptContext

# 加密算法
encrypt = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """
    密码加密

    :param password:
    :return:
    """
    return encrypt.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验

    :param plain_password:
    :param hashed_password:
    :return:
    """
    return encrypt.verify(plain_password, hashed_password)
