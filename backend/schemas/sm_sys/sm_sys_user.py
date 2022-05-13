#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from django.contrib.auth.models import User
from ninja import ModelSchema


class Login(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'password']


class CreateUser(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'password', 'email']


class UpdateUser(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'first_name', 'last_name', 'email']


class UpdateUserPassword(ModelSchema):
    class Config:
        model = User
        model_fields = ['password']


class GetUsers(ModelSchema):
    class Config:
        model = User
        model_exclude = ['password', 'groups', 'user_permissions']
