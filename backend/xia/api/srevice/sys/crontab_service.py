#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.xia.common.exception import errors
from backend.xia.crud.sys.crontab import SysCrontabDao
from backend.xia.schemas.sys.crontab import CreateCornTab, UpdateCornTab


def get_all_crontabs():
    return SysCrontabDao.get_all_crontab()


def get_crontab(pk: int):
    cron = SysCrontabDao.get_crontab_by_id(pk)
    if not cron:
        raise errors.NotFoundError(msg='定时任务不存在')
    return cron


def create(*, request, obj: CreateCornTab):
    cron = SysCrontabDao.create_crontab(obj, request.session['user'])
    return cron


def update(*, request, pk: int, obj: UpdateCornTab):
    cron = SysCrontabDao.get_crontab_by_id(pk)
    if not cron:
        raise errors.NotFoundError(msg='定时任务不存在')
    count = SysCrontabDao.update_crontab(pk, obj, request.session['user'])
    return count


def delete(pk: int):
    cron = SysCrontabDao.get_crontab_by_id(pk)
    if not cron:
        raise errors.NotFoundError(msg='定时任务不存在')
    count = SysCrontabDao.delete_crontab(pk)
    return count
