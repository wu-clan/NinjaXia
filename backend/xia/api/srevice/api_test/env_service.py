#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import Http404

from backend.xia.common.exception import errors
from backend.xia.crud.api_test.env import ApiTestEnvDao
from backend.xia.schemas.api_test.env import CreateApiTestEnv, UpdateApiTestEnv


def get_envs():
    return ApiTestEnvDao.get_all_envs()


def get_open_envs():
    return ApiTestEnvDao.get_all_enable_envs()


def get_env(pk: int):
    env = ApiTestEnvDao.get_env_by_id(pk)
    if not env:
        raise errors.NotFoundError(msg='环境不存在')
    return env


def create(*, request, obj: CreateApiTestEnv):
    env = ApiTestEnvDao.get_env_by_name(obj.name)
    if env:
        raise errors.ForbiddenError(msg='环境已存在, 请更换环境名称')
    new_env = ApiTestEnvDao.create_env(obj, request.session['user'])
    return new_env


def update(*, request, pk: int, obj: UpdateApiTestEnv):
    env = ApiTestEnvDao.get_env_by_id(pk)
    if not env:
        raise errors.NotFoundError(msg='环境不存在')
    if not env.name == obj.name:
        if ApiTestEnvDao.get_env_by_name(obj.name):
            raise errors.ForbiddenError(msg='环境已存在, 请更换环境名称')
    count = ApiTestEnvDao.update_env(pk, obj, request.session['user'])
    return count


def delete(pk: int):
    env = ApiTestEnvDao.get_env_by_id(pk)
    if not env:
        raise errors.NotFoundError(msg='环境不存在')
    count = ApiTestEnvDao.delete_env(pk)
    return count


def get_env_cases(pk: int):
    try:
        ApiTestEnvDao.get_env_or_404(pk)
    except Http404:
        raise errors.HTTP404('环境不存在')
    cases = ApiTestEnvDao.get_env_cases(pk)
    return cases
