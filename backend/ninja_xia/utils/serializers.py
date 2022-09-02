#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import orjson
from django.core.serializers import serialize
from django.db.models import QuerySet
from django.core.serializers.json import Serializer as DjangoSerializer
from django.utils.encoding import smart_str
from django.core.serializers import BUILTIN_SERIALIZERS

BUILTIN_SERIALIZERS['json'] = 'backend.utils.serializers'


class Serializer(DjangoSerializer):

    def get_dump_object(self, obj):
        """
        重写 get_dump_object() 方法，使得 id 和 model 返回字段不单独存储

        :param obj:
        :return:
        """
        self._current['id'] = smart_str(obj._get_pk_val(), strings_only=True)  # noqa
        self._current['model'] = smart_str(str(obj._meta))  # noqa
        return self._current


def serialize_data(data, to='json', use_list=False, **options):
    """
    Serialize a queryset (or any iterator that returns database objects) using
    a certain serializer.

    :param data: The data to serialize.
    :param to: serialization format, default is json.
    :param use_list: If True, the return result will be a list of objects.
    """
    if isinstance(data, QuerySet) and not use_list:
        return orjson.loads(serialize(to, data, **options))[0]
    if isinstance(data, QuerySet) and use_list:
        return orjson.loads(serialize(to, data, **options))
    if not isinstance(data, list) and not use_list:
        return orjson.loads(serialize(to, [data], **options))[0]
    return orjson.loads(serialize(to, [data], **options))
