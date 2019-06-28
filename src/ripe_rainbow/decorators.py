#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools

def test(
    description = None,
    script_url = None,
    bugs = []
):

    def decorator(function):

        function.test = True
        function.description = description or function.__name__
        function.script_url = script_url
        function.bugs = bugs

        @functools.wraps(function)
        def interceptor(*args, **kwargs):
            return function(*args, **kwargs)

        return interceptor

    return decorator
