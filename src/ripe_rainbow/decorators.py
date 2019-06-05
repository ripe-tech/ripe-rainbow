#!/usr/bin/python
# -*- coding: utf-8 -*-

def test(function):
    function.test = True
    function.description = function.__name__
    return function
