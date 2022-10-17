#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema
from pydantic import Field, validator


class CornTabBase(Schema):
    second: str = Field(..., regex=r'^(\*|(?:[0-9]$|([1-5][0-9]$)))')
    minute: str = Field(..., regex=r'^(\*|(?:[0-9]$|([1-5][0-9]$)))')
    hour: str = Field(..., regex=r'^(\*|(?:[0-9]$|1[0-9]$|2[0-3]$))')
    day: str = Field(..., regex=r'^(\*|(?:[1-9]$|([12][0-9])$|3[01]$))')
    month: str = Field(..., regex=r'^(\*|(?:[1-9]$|1[012]$))')
    day_of_week: str = Field(..., regex=r'^(\*|([0-6]$))')


class CreateCornTab(CornTabBase):
    pass


class UpdateCornTab(CornTabBase):
    pass


class GetAllCornTabs(CornTabBase):
    id: int
    create_user: int
    update_user: int = None
    created_time: datetime.datetime
    updated_time: datetime.datetime
