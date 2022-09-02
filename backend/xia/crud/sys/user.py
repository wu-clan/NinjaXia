#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone

from backend.xia.crud.base import CRUDBase
from backend.xia.schemas.sys.user import CreateUser, UpdateUser


class CRUDUser(CRUDBase[User, CreateUser, UpdateUser]):

    @staticmethod
    def get_user_by_username(username: str) -> User:
        return User.objects.filter(username=username).first()

    def get_user_by_id(self, pk: int) -> User:
        return super().get(pk=pk)

    @staticmethod
    def get_user_by_email(email: str) -> User:
        return User.objects.filter(email=email).first()

    @staticmethod
    def update_user_last_login(user: User) -> User:
        user.last_login = timezone.now()
        user.save()
        return user

    def put_user(self, pk: int, data: UpdateUser) -> User:
        return super().update_one(pk, data)

    @staticmethod
    def create_user(create_user: CreateUser) -> User:
        return User.objects.create_user(**create_user.dict())

    def get_all_users(self) -> QuerySet:
        return super().get_all()


UserDao = CRUDUser(User)
