#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import NinjaAPI

from backend.api.v1.project import project
from backend.api.v1.user import user
from backend.autoproject import settings

v1 = NinjaAPI(
    title=settings.NJ_TITLE,
    version=settings.NJ_VERSION,
    description=settings.NJ_DESCRIPTION,
    openapi_url=settings.NJ_OPENAPI_URL,
    docs_url=settings.NJ_DOCS_URL,
    csrf=settings.NJ_CSRF
)

v1.add_router('user/', user, tags=['用户'])
v1.add_router('project/', project, tags=['项目管理'])
