#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import loaders

class Runner(object):

    def __init__(self, loader = None):
        self.loader = loader or self.loader_default

    def run(self):
        raise appier.NotImplementedError()

    def test_suite(self):
        return self.loader.test_suite()

    @property
    def loader_default(self):
        return None

class ConsoleRunner(Runner):

    def run(self):
        for test in self.test_suite:
            try:
                print("Running test: %s" % str(test))
                test.run()
            except appier.AssertionError as exception:
                print("There was an error: %s" % str(exception))
            except Exception as exception:
                print("There was an exception: %s" % str(exception))

    @property
    def loader_default(self):
        return loaders.PathLoader(".")
