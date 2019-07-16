#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class SkipError(appier.AppierException):

    def __init__(self, *args, **kwargs):
        appier.AppierException.__init__(self, *args)
        self.reason = kwargs.get("reason", None)

class TimeoutError(appier.AppierException):
    pass

class ConsoleErrorsError(appier.AppierException):
    def __init__(self, *args, **kwargs):
        self.errors = kwargs.get("errors", None)
        separator = "\n\t"
        errors_s = separator.join("'%s'" % error["message"] for error in self.errors)

        appier.AppierException.__init__(
            self,
            *args,
            message = "Some errors were found in the console:%s%s" % (separator, errors_s)
        )
