#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional, Any, Union, Set, Dict

from django.db.models import QuerySet
from ninja import Schema
from pydantic import validate_arguments

from backend.ninja_xia.utils.encoder import jsonable_encoder
from backend.ninja_xia.utils.serializer import serialize_data

_JsonEncoder = Union[Set[Union[int, str]], Dict[Union[int, str], Any]]

__all__ = [
    'ResponseModel',
    'response_base'
]


class ResponseModel(Schema):
    """
    统一返回模型, 可以在接口请求中指定 response
    """
    code: int = 200
    msg: str = 'Success'
    data: Optional[Any] = None

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
        }


class ResponseBase:

    @staticmethod
    def _encode_json(data: Any):
        return jsonable_encoder(
            data,
            custom_encoder={
                datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
            }
        )

    @validate_arguments
    def success(self, *, code: int = 200, msg: str = 'Success', data: Optional[Any] = None, is_queryset: bool = False,
                exclude: Optional[_JsonEncoder] = None):
        """
        请求成功返回通用方法

        :param code: 返回状态码
        :param msg: 返回信息
        :param data: 返回数据
        :param is_queryset: 是否为 django QuerySet 模型
        :param exclude: 排除返回数据(data)字段
        :return:
        """
        if data is not None:
            if is_queryset:
                if isinstance(data, QuerySet):
                    data = serialize_data(data) if len(data) > 0 else None
                else:
                    data = self._encode_json(data)
            else:
                data = self._encode_json(data)
        return ResponseModel(code=code, msg=msg, data=data).dict(exclude={'data': exclude})

    @validate_arguments
    def fail(self, *, code: int = 400, msg: str = 'Bad Request', data: Any = None,
             exclude: Optional[_JsonEncoder] = None):
        if data is not None:
            data = self._encode_json(data)
        return ResponseModel(code=code, msg=msg, data=data).dict(exclude={'data': exclude})

    @validate_arguments
    def response_200(self, *, msg: str = 'Success', data: Optional[Any] = None, is_queryset: bool = False,
                     exclude: Optional[_JsonEncoder] = None):
        if data is not None:
            if is_queryset:
                if isinstance(data, QuerySet):
                    data = serialize_data(data) if len(data) > 0 else None
                else:
                    data = self._encode_json(data)
            else:
                data = self._encode_json(data)
        return ResponseModel(code=200, msg=msg, data=data).dict(exclude={'data': exclude})


response_base = ResponseBase()
