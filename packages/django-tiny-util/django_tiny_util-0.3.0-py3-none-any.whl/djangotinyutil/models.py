"""
Copyright (c) 2020 Oleg Bogumirski <reg@olegb.ru>
"""
from typing import Type

from django.db.models import Model


def get_or_none(model: Type[Model], **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
