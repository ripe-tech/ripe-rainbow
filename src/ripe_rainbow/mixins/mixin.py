#!/usr/bin/python
# -*- coding: utf-8 -*-

class Mixin(object):

    def __init__(self, owner):
        self.owner = owner

    @property
    def driver(self):
        return self.owner.driver
