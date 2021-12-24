#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from ninja import Schema


class ResponseBase(Schema):
    code: int = None
    data: Any = None


class Token(ResponseBase):
    token: str


class Message(ResponseBase):
    msg: str = None
