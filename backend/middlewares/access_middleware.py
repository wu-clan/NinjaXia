#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

from backend.common.log import log


class AccessMiddleware(MiddlewareMixin):
    """
    记录请求日志
    """

    def process_request(self, request):
        start_time = datetime.now()
        response = self.get_response(request)
        end_time = datetime.now()
        log.info(
            f"{response.status_code} {request.get_host()} {request.method} {request.path} {end_time - start_time}")
        return response
