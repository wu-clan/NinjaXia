#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from jinja2 import Template

from backend.ninja_xia.settings import REPORT_PATH


def render_testcase_report_html(file=REPORT_PATH, **kwargs):
    """
    渲染测试用例报告HTML

    :param file:
    :return:
    """
    with open(file, 'r', encoding='utf-8') as f:
        html = Template(f.read())

    return html.render(**kwargs)
