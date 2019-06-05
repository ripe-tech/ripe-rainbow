#!/usr/bin/python
# -*- coding: utf-8 -*-

class Part(object):

    def __init__(self, owner):
        self.owner = owner

    def __getattr__(self, name):
        if hasattr(self.owner, name):
            return getattr(self.owner, name)
        raise AttributeError("'%s' not found" % name)
