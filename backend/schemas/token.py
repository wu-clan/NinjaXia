#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Schema


class Token(Schema):
    code: int = None
    msg: str
    token: str
