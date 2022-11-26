#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from backend.xia.enums.base import IntEnum


class StateType(IntEnum):
    waiting = 0
    running = 1
    pause = 2
