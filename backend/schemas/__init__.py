#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from ninja import Schema


class ResponseBase(Schema):
    data: Any = None


class Token(ResponseBase):
    token: str


class Message(ResponseBase):
    code: int = None
    msg: str = None
