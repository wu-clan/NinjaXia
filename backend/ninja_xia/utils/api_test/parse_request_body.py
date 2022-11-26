#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from orjson import orjson
from orjson.orjson import JSONDecodeError

from backend.xia.enums.request.body import BodyType


def request_body_parser(*, params: str, cookies: str, headers: str, body_type: int, body: Any) -> dict:
    """
    请求体解析

    :param params:
    :param cookies:
    :param headers:
    :param body_type:
    :param body:
    :return:
    """
    try:
        params = orjson.loads(params) if params is not None else None
        cookies = orjson.loads(cookies) if cookies is not None else None
        headers = orjson.loads(headers) if headers is not None else None
        data = None
        files = None
        json = None

        if body_type == BodyType.none:
            data = data
            files = files
            json = json
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
                    headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                    data = orjson.loads(body)
                elif body_type == BodyType.graphQL:
                    headers.update({'Content-Type': 'application/json; charset=uft-8'})
                    json = orjson.loads(body)
                elif body_type == BodyType.text:
                    headers.update({'Content-Type': 'text/plain'})
                    data = body
                elif body_type == BodyType.js:
                    headers.update({'Content-Type': 'application/javascript'})
                    data = body
                elif body_type == BodyType.json:
                    headers.update({'Content-Type': 'application/json; charset=UTF-8'})
                    json = orjson.loads(body)
                elif body_type == BodyType.html:
                    headers.update({'Content-Type': 'text/html'})
                    data = body
                elif body_type == BodyType.xml:
                    headers.update({'Content-Type': 'application/xml'})
                    data = body
                else:
                    raise ValueError('请求数据格式错误')

        request_kwargs = {
            'params': params,
            'cookies': cookies,
            'headers': headers,
            'data': data,
            'files': files,
            'json': json
        }

    except JSONDecodeError as e:
        raise ValueError(f'请求体不是有效的 json 字符串: {e}')
    except Exception as e:
        raise RuntimeError(f'请求数据解析错误: {e}')

    return request_kwargs
