#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import traceback

from django.http import Http404
from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError, HttpError
from pydantic import ValidationError as PydanticValidationError

from backend.ninja_xia import settings
from backend.xia.common.exception.errors import BaseExceptionMixin
from backend.xia.common.response.response_schema import response_base


def _get_exception_code(status_code: int):
    return status_code if 100 <= status_code <= 599 else 400


def register_exception(app: NinjaAPI):
    @app.exception_handler(HttpError)
    def http_error_handler(request, exc: HttpError):
        return app.create_response(
            request,
            data=response_base.fail(code=exc.status_code, msg=exc.message),  # noqa
            status=_get_exception_code(exc.status_code),
        )

    @app.exception_handler(NinjaValidationError)
    def validation_error_handler(request, exc: NinjaValidationError):
        message = ''
        for error in exc.errors:
            field = str(error.get('loc')[-1])
            _msg = error.get('msg')
            message += f'{field} {_msg},'
        return app.create_response(
            request,
            data=response_base.fail(
                code=422,
                msg='请求参数非法' if len(message) == 0 else f'请求参数非法:{message[:-1]}',
                data=exc.errors if settings.DEBUG is True else None
            ),
            status=422,
        )

    @app.exception_handler(Http404)
    def http_404_handler(request, exc: Http404):
        msg = f'{exc.__str__()}' if len(exc.__str__()) != 0 else 'Not Found'
        return app.create_response(
            request,
            data=response_base.fail(code=404, msg=msg),
            status=404
        )

    @app.exception_handler(Exception)
    def all_exception_handler(request, exc: Exception):
        """
        全局异常处理

        :param request:
        :param exc:
        :return:
        """

        if isinstance(exc, PydanticValidationError):
            message = ''
            data = {}
            for raw_error in exc.raw_errors:
                if isinstance(raw_error.exc, PydanticValidationError):
                    exc = raw_error.exc
                    if hasattr(exc, 'model'):
                        fields = exc.model.__dict__.get('__fields__')
                        for field_key in fields.keys():
                            field_title = fields.get(field_key).field_info.title
                            data[field_key] = field_title if field_title else field_key
                    for error in exc.errors():
                        field = str(error.get('loc')[-1])
                        _msg = error.get('msg')
                        message += f'{data.get(field, field)} {_msg},'
                elif isinstance(raw_error.exc, json.JSONDecodeError):
                    message += 'json解析失败'
            return app.create_response(
                request,
                data=response_base.fail(
                    code=422,
                    msg='请求参数非法' if len(message) == 0 else f'请求参数非法:{message[:-1]}',
                    data={'errors': exc.errors()} if message == '' and settings.DEBUG is True else None
                ),
                status=422
            )

        if isinstance(exc, BaseExceptionMixin):
            return app.create_response(
                request,
                data=response_base.fail(
                    code=exc.code,
                    msg=str(exc.msg),
                    data=exc.data if exc.data else None
                ),
                status=_get_exception_code(exc.code),
            )

        else:
            return app.create_response(
                request,
                data=response_base.fail(code=500, msg=traceback.format_exc()) if settings.DEBUG else
                response_base.fail(code=500, msg='Internal Server Error'),
                status=500
            )
