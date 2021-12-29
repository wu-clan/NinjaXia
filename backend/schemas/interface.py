#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from enum import Enum

from ninja import Schema


class InterfaceBase(Schema):
    name: str
    description: str = None


class CreateInterface(Enum):

    @staticmethod
    def create():
        """写进函数避免循环引入模块问题,但是不起作用"""
        from backend.ninja_models.models.api_auto.interface import InterfaceCRUD
        for _name in InterfaceCRUD.select_project_by_pt_id():
            p_name = _name
            return p_name


class GetInterface(InterfaceBase):
    created_time: datetime.datetime
    modified_time: datetime.datetime
