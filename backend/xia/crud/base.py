#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import TypeVar, Generic, Type, Union, Dict, Any, List

from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from ninja import Schema

ModelType = TypeVar('ModelType', bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Schema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Schema)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, pk: int) -> ModelType:
        return self.model.objects.filter(id=pk).first()

    def get_object_or_404(self, pk: int) -> ModelType:
        return get_object_or_404(self.model, id=pk)

    def get_all(self) -> QuerySet:
        return self.model.objects.all()

    def get_values(self, *fields: str) -> List[dict]:
        return self.model.objects.values(*fields)

    def get_values_list(self, *fields, flat=False) -> List[Any]:
        return self.model.objects.values_list(*fields, flat=flat)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        return self.model.objects.create(**obj_in.dict())

    def update_one(self, pk: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        obj = self.get_object_or_404(pk)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict()
        for attr, value in update_data.items():
            setattr(obj, attr, value)
        obj.save()
        return obj

    def delete_one(self, pk: int) -> ModelType:
        obj = self.get_object_or_404(pk)
        obj.delete()
        return obj
