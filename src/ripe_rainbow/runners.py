#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import traceback

import appier
import appier_console

from . import loaders

class Runner(object):

    def __init__(self, loader = None, filter = None):
        self.loader = loader or self.loader_default
        self.filter = appier.conf("FILTER", filter)
        self.on_finish = []

        # creates the regular expression object that is going to
        # be used for test (method) name matching at runtime
        if self.filter: self.regex = re.compile("^.*%s.*$" % self.filter)
        else: self.regec = None

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
        # sets the default result flag value to valid as the execution
        # is considered to be valid by default
        result = True

        try:
            # iterates over the complete set of test cases for the test
            # suite that has been provided by the current loader to run
            # their respective tests, under the current runner
            for test_case in self.test_suite:

                # iterates over the complete set of test (methods) in the
                # test case to run then (if they are required)
                for test in test_case.tests:

                    # "gathers" the complete name for the test and verifies
                    # that it represents a valid one, against the regex
                    test_name = self._fullname(test)
                    if self.regex and not self.regex.match(test_name):
                        continue

                    # flushes the stdout and stderr so that the pending
                    # messages are properly handled by the output channels
                    sys.stdout.flush()
                    sys.stderr.flush()

                    try:
                        with appier_console.ctx_loader(
                            template = "{{spinner}} Running test: %s" % test_name
                        ):
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
