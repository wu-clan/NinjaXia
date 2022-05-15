#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Optional

import orjson
from django.http import Http404
from ninja import Schema, NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError
from ninja.errors import HttpError
from ninja.parser import Parser
from ninja.renderers import BaseRenderer
from pydantic import Field
from pydantic import ValidationError as PydanticValidationError


class ORJSONParser(Parser):
    """
    默认请求解析器
    """

    def parse_body(self, request):
        return orjson.loads(request.body)


class ORJSONRenderer(BaseRenderer):
    """
    默认响应渲染器
    """
    media_type = "application/json"

    def render(self, request, data, *, response_status):
        return orjson.dumps(data)


"""
说明：统一响应状态码
"""


class ResponseBase(Schema):
    data: Optional[Any] = None


class Response200(ResponseBase):
    code: int = 200
    msg: Optional[Any] = Field(default='Success')


class Response301(ResponseBase):
    code: int = 301
    msg: Optional[Any] = Field(default='Moved Permanently')


class Response400(ResponseBase):
    code: int = 400
    msg: Optional[Any] = Field(default='Bad Request')


class Response401(ResponseBase):
    code: int = 401
    msg: Optional[Any] = Field(default='Unauthorized')


class Response403(ResponseBase):
    code: int = 403
    msg: Optional[Any] = Field(default='Forbidden')


class Response404(ResponseBase):
    code: int = 404
    msg: Optional[Any] = Field(default='Not Found')


class Response500(ResponseBase):
    code: int = 500
    msg: Optional[Any] = Field(default='Internal Server Error')


class Response502(ResponseBase):
    code: int = 502
    msg: Optional[Any] = Field(default='Bad Gateway')


"""
说明：自定义响应状态码
"""


class Response40001(ResponseBase):
    code: int = 40001
    msg: Optional[Any] = Field(default='Request Validation Error')


"""
说明: 自定义异常
"""


class AuthorizationError(Exception):
    def __init__(self, err: str = 'Permission denied'):
        self.err = err


class TokenError(Exception):
    def __init__(self, err: str = 'Token is invalid'):
        self.err = err


"""
说明: 全局异常捕获
"""


def register_exception(app: NinjaAPI):
    @app.exception_handler(AuthorizationError)
    def authorization_error(request, exc: AuthorizationError):
        """
        用户权限异常
        :param request:
        :param exc:
        :return:
        """
        return app.create_response(
            request,
            data=Response401(msg=exc.err),
            status=401,
        )

    @app.exception_handler(TokenError)
    def token_error(request, exc: TokenError):
        """
        Token异常
        :param request:
        :param exc:
        :return:
        """
        return app.create_response(
            request,
            data=Response401(msg=exc.err),
            status=401,
        )

    @app.exception_handler(HttpError)
    def http_exception_handler(request, exc: HttpError):
        """
        全局HTTP异常处理
        :param request:
        :param exc:
        :return:
        """
        return app.create_response(
            request,
            data=Response400(code=exc.status_code, msg="".join(exc.args)),
            status=exc.status_code,
        )

    @app.exception_handler(Http404)
    def http_exception_handler(request, exc: Http404):
        """
        全局HTTP404异常处理
        :param request:
        :param exc:
        :return:
        """
        return app.create_response(
            request,
            data=Response404(msg="".join(exc.args)),
            status=404,
        )

    # @app.exception_handler(Exception)
    # def all_exception_handler(request, exc: Exception):
    #     """
    #     全局异常处理
    #     :param request:
    #     :param exc:
    #     :return:
    #     """
    #     return app.create_response(
    #         request,
    #         data=Response500(msg="".join(exc.args)),
    #         status=500,
    #     )

    @app.exception_handler(NinjaValidationError)
    def validation_error(request, exc: NinjaValidationError):
        """
        Ninja全局请求数据验证异常处理
        :param request:
        :param exc:
        :return:
        """
        return app.create_response(
            request,
            data=Response40001(data={'body': exc.args, 'errors': exc.errors}),
            status=422,
        )

    @app.exception_handler(PydanticValidationError)
    def validation_error(request, exc: PydanticValidationError):
        """
        Pydantic全局请求数据验证异常处理
        :param request:
        :param exc:
        :return:
        """
        return app.create_response(
            request,
            data=Response40001(data={'errors': exc.errors()}),
            status=422,
        )
