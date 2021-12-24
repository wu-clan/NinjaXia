#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.contrib.auth.models import User
from ninja import ModelSchema, Schema
from pydantic import EmailStr


class Login(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'password']


class CreateUser(ModelSchema):
    groups: List[Login] = []

    class Config:
        model = User
        model_fields = ['email']
