#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from ninja import Router
from ninja.pagination import paginate

from backend.common.pagination import CustomPagination
from backend.crud.v1.crud_api_test.crud_api_test_task import crud_api_test_task
from backend.schemas.v1.sm_api_test.sm_api_test_task import GetAllApiTestTasks

v1_api_test_task = Router()


@v1_api_test_task.get('/all', summary='获取所有模块', response=List[GetAllApiTestTasks])
@paginate(CustomPagination)
def get_all_tasks(request):
    return crud_api_test_task.get_all_tasks()
