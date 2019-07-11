#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import traceback

import appier

from . import util

class Result(object):

    def __init__(
        self,
        test,
        result = "success",
        exception = None,
        stacktrace = None
    ):
        object.__init__(self)
        self.test = test
        self.result = result
        self.exception = exception
        self.stacktrace = stacktrace

    @classmethod
    def build_success(cls, test):
        return cls(test, result = "success")

    @classmethod
    def build_skip(cls, test):
        return cls(test, result = "skip")

    @classmethod
    def build_failure(cls, test, exception):
        lines = traceback.format_exc().splitlines()
        lines = [line.decode("utf-8", "ignore") if appier.legacy.is_bytes(line) else\
            line for line in lines]
        return cls(
            test,
            result = "failure",
            exception = exception,
            stacktrace = lines
        )

    def print_result(self, file = sys.stdout):
        file.write("----------------------------\n")
        file.write(util.test_fullname(self.test) + "\n")
        if self.exception: file.write(str(self.exception) + "\n")
        for line in self.stacktrace if self.stacktrace else []:
            file.write(line + "\n")

    @property
    def failure(self):
        return not self.success

    @property
    def success(self):
        return self.result == "success"
