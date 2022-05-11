#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

from backend.api.v1.v1_project import project
from backend.api.v1.v1_user import user

v1 = Router()

v1.add_router('/user', user, tags=['用户'])
v1.add_router('/project', project, tags=['项目管理'])
