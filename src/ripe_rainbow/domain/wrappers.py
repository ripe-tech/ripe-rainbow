#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import base
from . import logic

BASE_TUPLES = (
    ("assertions", base.AssertionsPart),
    ("interactions", base.InteractionsPart),
    ("waits", base.WaitsPart)
)

COPPER_TUPLES = (
    ("id", logic.RipeIdPart),
    ("core", logic.RipeCorePart),
    ("copper", logic.RipeCopperPart)
)

PULSE_TUPLES = (
    ("id", logic.RipeIdPart),
    ("core", logic.RipeCorePart),
    ("pulse", logic.RipePulsePart)
)

RETAIL_TUPLES = (
    ("admin", logic.AdminPart),
    ("core", logic.RipeCorePart),
    ("retail", logic.RipeRetailPart)
)

WHITE_TUPLES = (
    ("core", logic.RipeCorePart),
    ("white", logic.RipeWhitePart)
)

class DomainWrapper(object):

    @classmethod
    def wrap(cls, instance, tuples):
        for name, _cls in tuples:
            part = _cls(instance)
            setattr(instance, name, part)

    @classmethod
    def wrap_base(cls, instance):
        cls.wrap(instance, BASE_TUPLES)

    @classmethod
    def wrap_copper(cls, instance):
        cls.wrap(instance, COPPER_TUPLES)

    @classmethod
    def wrap_pulse(cls, instance):
        cls.wrap(instance, PULSE_TUPLES)

    @classmethod
    def wrap_retail(cls, instance):
        cls.wrap(instance, RETAIL_TUPLES)

    @classmethod
    def wrap_white(cls, instance):
        cls.wrap(instance, WHITE_TUPLES)
