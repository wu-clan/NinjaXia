#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.xia.enums.base import StrEnum


class MethodType(StrEnum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
