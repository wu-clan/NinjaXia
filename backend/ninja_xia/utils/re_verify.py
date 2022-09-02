#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern, text) -> bool:
    result = re.search(pattern, text)
    if result:
        return True
    else:
        return False


def match_string(pattern, text) -> bool:
    result = re.match(pattern, text)
    if result:
        return True
    else:
        return False


def check_crontab(text: str) -> None:
    """
    校验 crontab 格式
    :param text:
    :return:
    """
    values = text.split()
    if len(values) != 6:
        raise ValueError('corn表达式格式不符合规范, 请查看使用说明')
    second = match_string(r'^(\*|(?:[0-9]$|([1-5][0-9]$)))', values[0])
    minute = match_string(r'^(\*|(?:[0-9]$|([1-5][0-9]$)))', values[1])
    hour = match_string(r'^(\*|(?:[0-9]$|1[0-9]$|2[0-3]$))', values[2])
    day = match_string(r'^(\*|(?:[1-9]$|([12][0-9])$|3[01]$))', values[3])
    month = match_string(r'^(\*|(?:[1-9]$|1[012]$))', values[4])
    day_of_week = match_string(r'^(\*|([0-6]$))', values[5])
    if not all(_ for _ in [second, minute, hour, day, month, day_of_week]):
        raise ValueError('corn表达式错误')
