#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from orjson import orjson

from backend.xia.enums.request.body import BodyType


def request_body_parser(headers: dict, body_type: int, body: Any) -> dict:
    """
    请求体解析

    :param headers:
    :param body_type:
    :param body:
    :return:
    """

    # 解析请求body
    data = {}
    files = {}
    content = None
    json = {}

    if body_type == BodyType.none:
        data = None
        files = None
        json = None
    else:
        if body is not None:
            if body_type == BodyType.form:
                items = orjson.loads(body)
                for item in items:
                    if item.get('type') == 'string':
                        data = data.update({item.get('key'): item.get('value', '')})
                    elif item.get('type') == 'integer':
                        data = data.update(
                            {item.get('key'): int(item.get('value')) if item.get('value') is not None else None})
                    elif item.get('type') == 'file':
                        if isinstance(item.get('value'), list):
                            files = files.update({item.get('key'): [open(_, 'rb') for _ in item.get('value')]})
                        else:
                            files = files.update({item.get('key'): open(item.get('value'), 'rb')})
            elif body_type == BodyType.x_form:
                if "Content-Type" not in headers:
                    headers['Content-Type'] = 'application/x-www-form-urlencoded'
                else:
                    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                data = orjson.loads(body)
            elif body_type == BodyType.binary:
                content = body
            elif body_type == BodyType.graphQL:
                data = body
            elif body_type == BodyType.text:
                content = body
            elif body_type == BodyType.js:
                content = body
            elif body_type == BodyType.json:
                if "Content-Type" not in headers:
                    headers['Content-Type'] = 'application/json; charset=UTF-8'
                else:
                    headers.update({'Content-Type': 'application/json; charset=UTF-8'})
                data = orjson.loads(body)
            elif body_type == BodyType.html:
                content = body
            elif body_type == BodyType.xml:
                content = body
            else:
                raise ValueError('请求数据格式错误')

    request_kwargs = {
        'data': data,
        'files': files,
        'json': json,
        'content': content
    }

    return request_kwargs
