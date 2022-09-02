#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

import orjson
from django.http import HttpRequest
from ninja.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    """
    orjson 响应渲染器
    """
    media_type = "application/json"

    def render(self, request: HttpRequest, data: Any, *, response_status: int) -> Any:
        return orjson.dumps(data)
