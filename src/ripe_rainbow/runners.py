#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import traceback

import appier

from . import loaders

class Runner(object):

    def __init__(self, loader = None):
        self.loader = loader or self.loader_default

    def run(self):
        raise appier.NotImplementedError()

    @property
    def test_suite(self):
        return self.loader.test_suite()

    @property
    def loader_default(self):
        return None

class ConsoleRunner(Runner):

    def run(self):
        for test_case in self.test_suite:
            for test in test_case.tests:
                print("Running test: %s" % str(test))
                try:
                    test_case.run_test(test)
                except appier.AssertionError as exception:
                    print("There was an error: %s" % str(exception))
                except Exception as exception:
                    print("There was an exception: %s" % str(exception))
                    print("Exception in user code:")
                    print("-" * 60)
                    traceback.print_exc(file = sys.stdout)
                    print("-" * 60)

    @property
    def loader_default(self):
        return loaders.PathLoader(".")
