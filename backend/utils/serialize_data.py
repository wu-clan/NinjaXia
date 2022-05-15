#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import orjson
from django.core.serializers import serialize
from django.db.models import QuerySet


def serialize_data(data, use_list=False):
    """
    Serialize a queryset (or any iterator that returns database objects) using
    a certain serializer.

    :param data: The data to serialize.
    :param use_list: If True, the serializer will be used for a list of objects.
    """
    if isinstance(data, QuerySet):
        return orjson.loads(serialize('json', data))
    if not isinstance(data, list) and use_list is False:
        return orjson.loads(serialize('json', [data]))[0]
    return orjson.loads(serialize('json', [data]))
