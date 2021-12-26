#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Schema


class ProjectBase(Schema):
    name: str
    description: str = None


class UpdateProject(ProjectBase):
    name: str = None
    description: str = None
