#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from ninja import Router

module = Router()


@module.get('/')
def get_all_modules(request):
    ...