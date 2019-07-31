#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import time

import appier
import appier_console

from . import util
from . import info
from . import errors
from . import loaders
from . import results

class Runner(object):

    def __init__(self, loader = None, filter = None):
        self.loader = loader or self.loader_default
        self.filter = appier.conf("FILTER", filter)
        self.repeat = appier.conf("REPEAT", 1, cast = int)
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
        start_g = time.time()
        result = True
        passed = 0
        skipped = 0
        failed = 0
        passes = []
        skips = []
        failures = []

        # prints the header information on the product to be used to indicate
        # the proper execution of then console
        print(info.LABEL)
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

                    # iterates over the amount of time the test should be run
                    # this is relevant for stress testing based execution
                    for index in appier.legacy.xrange(self.repeat):

                        # "gathers" the complete name for the test and verifies
                        # that it represents a valid one, against the regex
                        test_name = util.test_fullname(test)
                        if self.regex and not self.regex.match(test_name):
                            continue

                        # in case the name of the test case class is not printed
                        # runs the printing operation and unsets the flag
                        if not printed:
                            print("    %s" % util.test_case_fullname(test_case))
                            printed = True

                        # stores the starting time for the execution so that it's
                        # latter possible to calculate the duration of the test
                        start = time.time()

                        # builds the string prefix for the test to be used in the
                        # printing of the label for test execution
                        test_prefix = "[%d] " % (index + 1) if self.repeat > 1 else ""

                        try:
                            # starts the appier console context loader so that an animation
                            # is executed while the test is running (where it's possible)
                            with appier_console.ctx_loader(
                                spinner = "dots3",
                                template = "        %s%s {{spinner}}" % (test_prefix, test_name),
                                single = True,
                                eol = ""
                            ):
                                # executes the concrete logic of the test, making sure
                                # that an overall spinner is making the UI interactive
                                test_case.run_test(test)

                            test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_CYAN)
                            mark_s = appier_console.colored("√", color = appier_console.COLOR_GREEN)
                            extra_s = ""
                            success = results.Result.build_success(test)
                            passes.append(success)
                            passed += 1
                        except errors.SkipError as exception:
                            test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_CYAN)
                            mark_s = appier_console.colored("~", color = appier_console.COLOR_CYAN)
                            extra_s = " (" + exception.reason + ")" if exception.reason else ""
                            skip = results.Result.build_skip(test)
                            skips.append(skip)
                            skipped += 1
                        except appier.AssertionError as exception:
                            result = False
                            test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_RED)
                            mark_s = appier_console.colored("✗", color = appier_console.COLOR_RED)
                            if test.bugs: extra_s = " (" + ", ".join(bug["url"] for bug in test.bugs if "url" in bug) + ")"
                            else: extra_s = ""
                            failure = results.Result.build_failure(test, exception)
                            failures.append(failure)
                            failed += 1
                        except Exception as exception:
                            result = False
                            failure = results.Result.build_failure(test, exception)
                            failures.append(failure)
                            test_name_s = appier_console.colored(test_name, color = appier_console.COLOR_RED)
                            mark_s = appier_console.colored("✗", color = appier_console.COLOR_RED)
                            if test.bugs: extra_s = " (" + ", ".join(bug["url"] for bug in test.bugs if "url" in bug) + ")"
                            else: extra_s = ""
                            failed += 1

                        # determines the kind of environment we're running on and taking that
                        # into account prints the proper output, standard is tty environment
                        # meaning that proper interaction is allowed
                        if appier_console.is_tty():
                            print("        %s %s%s%s" % (test_name_s, mark_s, extra_s, self._duration(start)))

                        # otherwise we're in a textual environment and only the extra part of
                        # the line is expected to be printed (not possible to go back in the line)
                        else:
                            print("%s%s%s" % (mark_s, extra_s, self._duration(start)))

                        # flushes the stdout and stderr so that the pending
                        # messages are properly handled by the output channels
                        sys.stdout.flush()
                        sys.stderr.flush()

                if printed: print("")
        finally:
            self.run_on_finish()

        passed_s = appier_console.colored(
            "%d passing" % passed,
            color = appier_console.COLOR_GREEN
        ) if passed else ""
        skipped_s = appier_console.colored(
            "%d skipped" % skipped,
            color = appier_console.COLOR_CYAN
        ) if skipped else ""
        failed_s = appier_console.colored(
            "%d failing" % failed,
            color = appier_console.COLOR_RED
        ) if failed else ""
        duration_s = self._duration(start_g, info = 0.0, warning = 3600.0, error = 14400.0)
        print("  %s%s%s%s%s" % (
                " " + passed_s if passed_s else "",
                " " + skipped_s if skipped_s else "",
                " " + failed_s if failed_s else "",
                "No tests executed" + failed_s if not passed_s and not skipped_s and not failed_s else "",
                duration_s
            )
        )

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

    def _duration(self, start, info = 5.0, warning = 5.0, error = 10.0):
        duration = time.time() - start
        if duration < info: return ""
        if duration >= error: color = appier_console.COLOR_RED
        elif duration >= warning: color = appier_console.COLOR_YELLOW
        else: color = appier_console.COLOR_CYAN
        return appier_console.colored(" (%.02fs)" % duration, color = color)

    @property
    def loader_default(self):
        return loaders.PathLoader(".")
