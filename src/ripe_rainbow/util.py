#!/usr/bin/python
# -*- coding: utf-8 -*-

def test_case_fullname(test_case, use_ctx = True):
    use_ctx = use_ctx and hasattr(test_case, "ctx")
    ctx = test_case.ctx if use_ctx else None
    ctx_s = "%s." % ctx if ctx else ""
    module = test_case.__class__.__module__
    if module == None or module == str.__class__.__module__:
        return ctx_s + test_case.__class__.__name__
    return ctx_s + module + "." + test_case.__class__.__name__

def test_fullname(test, use_ctx = False):
    instance = test.__self__
    return test_case_fullname(instance, use_ctx = use_ctx) + "." + test.__name__
