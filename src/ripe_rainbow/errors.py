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
        tabs = kwargs.get("tabs")
        self.reason = "Tab %s doesn't exist, there are only %s tabs" % (tab, tabs)
