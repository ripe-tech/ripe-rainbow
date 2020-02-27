#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class SkipError(appier.AppierException):

    def __init__(self, *args, **kwargs):
        appier.AppierException.__init__(self, *args)
        self.reason = kwargs.get("reason", None)

class TimeoutError(appier.AppierException):
    pass

class CloseTabError(appier.AppierException):
    pass

class UnexistingTabError(CloseTabError):

    def __init__(self, *args, **kwargs):
        appier.AppierException.__init__(self, *args)
        tab = kwargs.get("tab")
        tab_count = kwargs.get("tab_count")
        self.reason = "Tab '%s' doesn't exist, there are only %d tabs" % (tab, tab_count)
