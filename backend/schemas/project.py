#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

from ninja import Schema


class ProjectBase(Schema):
    name: str
    is_active: bool
    description: str = None


class UpdateProject(ProjectBase):
    name: str = None


class GetProject(ProjectBase):
    is_active: bool
    created_time: datetime.datetime
    modified_time: datetime.datetime
