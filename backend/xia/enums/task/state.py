#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import IntEnum


class StateType(IntEnum):
    unopened = 0
    pending = 1
    running = 2
    pause = 3
