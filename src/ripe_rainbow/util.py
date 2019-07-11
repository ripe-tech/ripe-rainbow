#!/usr/bin/python
# -*- coding: utf-8 -*-

def test_case_fullname(test_case):
    module = test_case.__class__.__module__
    if module == None or module == str.__class__.__module__:
        return test_case.__class__.__name__
    return module + "." + test_case.__class__.__name__

def test_fullname(test):
    instance = test.__self__
    module = instance.__class__.__module__
    if module == None or module == str.__class__.__module__:
        return instance.__class__.__name__ + "." + test.__name__
    return module + "." + instance.__class__.__name__ + "." + test.__name__
