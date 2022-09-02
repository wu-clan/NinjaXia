#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.http import Http404
from ninja import NinjaAPI
from ninja.errors import HttpError

from backend.xia.common.exception.exception_class import AuthorizationException, TokenException
from backend.xia.common.log import log
from backend.xia.common.response.response_schema import Response422, Response500, Response404, Response400, Response401
from ninja.errors import ValidationError as NinjaValidationError
from pydantic import ValidationError as PydanticValidationError


def register_exception(app: NinjaAPI):
    @app.exception_handler(AuthorizationException)
    def authorization_error(request, exc: AuthorizationException):
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

    @app.exception_handler(TokenException)
    def token_error(request, exc: TokenException):
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
        err_msg = "".join(exc.args)
        log.error(err_msg)
        return app.create_response(
            request,
            data=Response400(code=exc.status_code, msg=err_msg),
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

    @app.exception_handler(Exception)
    def all_exception_handler(request, exc: Exception):
        """
        全局异常处理

        :param request:
        :param exc:
        :return:
        """
        err_msg = "".join(exc.args)
        log.error(err_msg)
        return app.create_response(
            request,
            data=Response500(msg=err_msg),
            status=500,
        )

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
            data=Response422(data={'body': exc.args, 'errors': exc.errors}),
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
            data=Response422(data={'errors': exc.errors()}),
            status=422,
        )
