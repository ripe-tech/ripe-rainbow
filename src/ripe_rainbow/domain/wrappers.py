#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import base

LOGIC_TUPLES = (
    ("assertions", base.AssertionsPart),
    ("interactions", base.InteractionsPart),
    ("waits", base.WaitsPart)
)

class DomainWrapper(object):

    @classmethod
    def wrap_logic(cls, instance):
        for name, cls in LOGIC_TUPLES:
            part = cls(instance)
            setattr(instance, name, part)
