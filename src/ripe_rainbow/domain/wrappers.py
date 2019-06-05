#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import base
from . import logic

BASE_TUPLES = (
    ("assertions", base.AssertionsPart),
    ("interactions", base.InteractionsPart),
    ("waits", base.WaitsPart)
)

RETAIL_TUPLES = (
    ("admin", logic.AdminPart),
    ("retail", logic.RetailPart)
)

class DomainWrapper(object):

    @classmethod
    def wrap_base(cls, instance):
        for name, cls in BASE_TUPLES:
            part = cls(instance)
            setattr(instance, name, part)

    @classmethod
    def wrap_retail(cls, instance):
        for name, cls in RETAIL_TUPLES:
            part = cls(instance)
            setattr(instance, name, part)
