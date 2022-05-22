#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import NinjaAPI

from backend.api.v1 import v1
from backend.ninja_xia import settings
from backend.schemas import ORJSONRenderer, register_exception, ORJSONParser


def register_app():
    """
    注册应用
    :return:
    """
    app = NinjaAPI(
        title=settings.NINJA_TITLE,
        version=settings.NINJA_VERSION,
        description=settings.NINJA_DESCRIPTION,
        openapi_url=settings.NINJA_OPENAPI_URL,
        docs_url=settings.NINJA_DOCS_URL,
        csrf=settings.NINJA_CSRF,
        parser=ORJSONParser(),
        # renderer=ORJSONRenderer(),
    )

    # 路由
    register_router(app)

    # 全局异常处理
    register_exception(app)

    return app


def register_router(app: NinjaAPI):
    """
    注册路由

    :param app:
    :return:
    """
    app.add_router('', v1)
