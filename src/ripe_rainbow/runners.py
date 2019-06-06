#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

import appier
import appier_console

from . import util
from . import loaders
from . import results

class Runner(object):

    def __init__(self, loader = None, filter = None):
        self.loader = loader or self.loader_default
        self.filter = appier.conf("FILTER", filter)
        self.on_finish = []

        # creates the regular expression object that is going to
        # be used for test (method) name matching at runtime
        if self.filter: self.regex = re.compile("^.*%s.*$" % self.filter)
        else: self.regex = None

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
        passed = 0
        failed = 0
        passes = []
        failures = []

        # prints the header information on the product to be used to indicate
        # the proper execution of then console
        print("RIPE Rainbow 🌈")
        print("")

        try:
            # iterates over the complete set of test cases for the test
            # suite that has been provided by the current loader to run
            # their respective tests, under the current runner
            for test_case in self.test_suite:

                # sets the printed (overhead) flag as false indicating that
                # the name of the class is still pending printing
                printed = False

                # iterates over the complete set of test (methods) in the
                # test case to run then (if they are required)
                for test in test_case.tests:

                    # "gathers" the complete name for the test and verifies
                    # that it represents a valid one, against the regex
                    test_name = util.test_fullname(test)
                    if self.regex and not self.regex.match(test_name):
                        continue

                    # in case the name of the test case class is not printed
                    # runs the printing operation and unsets the flag
                    if not printed:
                        print("    %s" % test_case.__class__.__name__)
                        printed = True

                    # flushes the stdout and stderr so that the pending
                    # messages are properly handled by the output channels
                    sys.stdout.flush()
                    sys.stderr.flush()

                    try:
                        with appier_console.ctx_loader(
                            spinner = "dots3",
                            template = "        %s {{spinner}}" % test_name,
                            single = True
                        ):
                            test_case.run_test(test)

                        test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_GRAY)
                        print("        %s ✔️" % test_name_s)
                        result = results.Result.build_success(test)
                        passes.append(result)
                        passed += 1
                    except appier.AssertionError as exception:
                        result = False
                        test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_RED)
                        print("        %s ❌️" % test_name_s)
                        result = results.Result.build_failure(test, exception)
                        failures.append(result)
                        failed += 1
                    except Exception as exception:
                        result = False
                        result = results.Result.build_failure(test, exception)
                        failures.append(result)
                        test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_RED)
                        print("        %s ❌️" % test_name_s)
                        failed += 1

                if printed: print("")
        finally:
            self.run_on_finish()

        passed_s = appier_console.colored(
            "%d passing" % passed,
            color = appier_console.COLOR_GREEN
        ) if passed else ""
        failed_s = appier_console.colored(
            "%d failing" % failed,
            color = appier_console.COLOR_RED
        ) if failed else ""
        print("  %s %s" % (passed_s, failed_s))

        # iterates over the complete set of failures to print
        # their description for better understanding of the
        # the underlying issues
        if failures: print("")
        for failure in failures: failure.print_result()

        print("")

        if result:
            print("The sky is blue and the sun is shining ☀️")
        else:
            print("There are some clouds in the sky 🌧️")

        return result

    @property
    def loader_default(self):
        return loaders.PathLoader(".")
