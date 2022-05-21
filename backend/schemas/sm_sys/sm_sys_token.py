#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ninja import Schema


class Token(Schema):
    code: int = 200
    msg: str = None
    access_token: str
    token_type: str
    is_superuser: bool = None
