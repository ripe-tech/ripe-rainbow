#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools

def test(
    description = None,
    script_url = None,
    bug = None,
    bugs = []
):

    # in case the bugs are not defined tries to fallback
    # to the (single) bug parameter (convenience) and then
    # ensures that the bugs are set as a sequence
    if not bugs: bugs = [bug] if bug else bugs
    if not isinstance(bugs, (list, tuple)): bugs = [bugs]

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
