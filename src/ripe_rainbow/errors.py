#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class SkipError(appier.AppierException):

    def __init__(self, *args, **kwargs):
        appier.AppierException.__init__(self, *args)
        self.reason = kwargs.get("reason", None)

class TimeoutError(appier.AppierException):
    pass
