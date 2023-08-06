"""
Copyright (c) 2020 Oleg Bogumirski <reg@olegb.ru>
"""


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
