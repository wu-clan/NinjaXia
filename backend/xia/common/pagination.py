#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from typing import List, Any

from ninja import Schema, Field
from ninja.pagination import PaginationBase

"""
自定义分页类
docs: https://django-ninja.rest-framework.com/tutorial/pagination/#creating-custom-pagination-class
"""


class CustomPagination(PaginationBase):
    class Input(Schema):
        page: int = Field(1, gt=0, description='当前页码')
        size: int = Field(10, gt=0, le=100, description='每页数量')

    class Output(Schema):
        items: List[Any] = Field(..., description='数据')
        count: int = Field(..., description='总数据数')
        page: int = Field(..., description='当前页码')
        size: int = Field(..., description='每页显示数量')
        next: str = Field(..., description='下一页url')
        previous: str = Field(..., description='上一页url')
        total_pages: int = Field(..., description='总页数')

    def paginate_queryset(self, queryset, pagination: Input, **params) -> Any:
        page = pagination.page
        size = pagination.size
        offset = (page - 1) * size
        items = queryset[offset: offset + size]
        count = self._items_count(queryset)
        total_pages = math.ceil(count / size)
        return {
            "items": items,
            "count": count,
            'page': page,
            'size': size,
            'next': f"?page={page + 1}&size={size}" if (page + 1) <= total_pages else "null",
            'previous': f"?page={page - 1}&size={size}" if (page - 1) >= 1 else "null",
            'total_pages': total_pages,
        }
