#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import traceback

import appier

from . import loaders

class Runner(object):

    def __init__(self, loader = None):
        self.loader = loader or self.loader_default
        self.on_finish = []

    def run(self):
        raise appier.NotImplementedError()

    def add_on_finish(self, method):
        self.on_finish.append(method)

    def remove_on_finish(self, method):
        self.on_finish.remove(method)

    def run_on_finish(self):
        for method in self.on_finish:
            method()

    @property
    def test_suite(self):
        return self.loader.test_suite(runner = self)

    @property
    def loader_default(self):
        return None

class ConsoleRunner(Runner):

    def run(self):
        result = True
        try:
            for test_case in self.test_suite:
                for test in test_case.tests:
                    print("Running test: %s" % self._fullname(test))
                    try:
                        test_case.run_test(test)
                    except appier.AssertionError as exception:
                        result = False
                        print("There was an error: %s" % str(exception))
                    except Exception as exception:
                        result = False
                        print("There was an exception: %s" % str(exception))
                        print("Exception in user code:")
                        print("-" * 60)
                        traceback.print_exc(file = sys.stdout)
                        print("-" * 60)
        finally:
            self.run_on_finish()

        return result

    @property
    def loader_default(self):
        return loaders.PathLoader(".")

    def _fullname(self, method):
        instance = method.__self__
        module = instance.__class__.__module__
        if module == None or module == str.__class__.__module__:
            return instance.__class__.__name__ + "." + method.__name__
        return module + "." + instance.__class__.__name__ + "." + method.__name__
