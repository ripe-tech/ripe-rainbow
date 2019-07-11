#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class SkipError(appier.AppierException):
    pass

class TimeoutError(appier.AppierException):
    pass
