#!/usr/bin/python
# -*- coding: utf-8 -*-

class Part(object):

    def __init__(self, owner):
        self.owner = owner

    @property
    def timeout(self):
        return self.owner.timeout

    @property
    def driver(self):
        return self.owner.driver
