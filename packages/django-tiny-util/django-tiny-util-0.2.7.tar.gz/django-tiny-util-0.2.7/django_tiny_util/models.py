"""
Copyright (c) 2020 Oleg Bogumirski <reg@olegb.ru>
"""
from typing import Optional

from django.db.models import Model


def get_or_none(cls: type(Model), **kwargs) -> Optional[Model]:
    try:
        return cls.objects.get(**kwargs)
    except cls.DoesNotExist:
        return None


def update_fields(model: Model, **kwargs):
    if kwargs.get('filter_fields'):
        fields = [x for x, y in kwargs.items() if x in [z.name for z in model._meta.get_fields(include_hidden=True)]]
    else:
        fields = list(kwargs.keys())

    for key in fields:
        setattr(model, key, kwargs[fields])

    model.save(update_fields=fields)
