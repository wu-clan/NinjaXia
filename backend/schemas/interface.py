#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from enum import Enum

from ninja import Schema
from pydantic import Field


class InterfaceBase(Schema):
    name: str
    description: str = None


class CreateInterface(Schema):
    id: int = Field(default=1, description='外键项目主键')


class UpdateInterface(CreateInterface):
    pass


class GetInterface(InterfaceBase):
    id: int
    created_time: datetime.datetime
    modified_time: datetime.datetime
