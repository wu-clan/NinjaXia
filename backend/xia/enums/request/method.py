#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum


class MethodType(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
