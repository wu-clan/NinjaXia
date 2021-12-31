#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
from enum import Enum

from ninja import Schema


class InterfaceBase(Schema):
    name: str
    description: str = None


class GetInterface(InterfaceBase):
    created_time: datetime.datetime
    modified_time: datetime.datetime
