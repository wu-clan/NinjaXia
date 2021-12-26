#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from ninja import Schema


class Message(Schema):
    code: int = None
    msg: str = None
    data: Any = None
