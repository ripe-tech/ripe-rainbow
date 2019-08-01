#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import traceback

import appier

from . import drivers

from .. import util
from .. import test_cases

class InteractiveTestCase(test_cases.TestCase):

    def __init__(self, *args, **kwargs):
        test_cases.TestCase.__init__(self, *args, **kwargs)
        self.options = kwargs
        self.driver = None
        self.timeout = appier.conf("TIMEOUT", 15, cast = int)
        self.timeout = self.options.get("timeout", self.timeout)

    def before(self):
        test_cases.TestCase.before(self)
        self.driver = self.load_driver()

    def after(self):
        if self.driver:
            self.driver.stop()
            self.driver = None
        test_cases.TestCase.after(self)

    def failed(self, test, exception, ctx = None):
        test_cases.TestCase.failed(self, test, exception)
        self._stacktrace(test, ctx = ctx)
        self._screenshot(test, ctx = ctx)

    def load_driver(self, start = True):
        driver_s = appier.conf("DRIVER", "selenium")
        driver_s = self.options.get("driver", driver_s)
        driver = drivers.InteractiveDriver.driver_g(driver_s)(self)
        if start: driver.start()
        return driver

    def _stacktrace(self, test, ctx = None):
        if not appier.conf("STACKTRACES", False, cast = bool): return
        if not self.driver: return
        ctx = ctx or {}
        index = ctx.get("index", 0)
        repeat = ctx.get("repeat", 1)
        extra_s = "-%d" % (index + 1) if repeat > 1 else ""
        base_path = appier.conf("STACKTRACES_PATH", ".")
        lines = traceback.format_exc().splitlines()
        lines = [line.decode("utf-8", "ignore") if appier.legacy.is_bytes(line) else\
            line for line in lines]
        test_name = util.test_fullname(test)
        if not os.path.exists(base_path): os.makedirs(base_path)
        stack_path = os.path.join(base_path, test_name + extra_s + ".log")
        stack_path = os.path.abspath(stack_path)
        stack_path = os.path.normpath(stack_path)
        stack_file = open(stack_path, "wb")
        try:
            for line in lines:
                stack_file.write(line.encode("utf-8"))
                stack_file.write(b"\n")
        finally:
            stack_file.close()

    def _screenshot(self, test, ctx = None):
        if not appier.conf("SCREENSHOTS", False, cast = bool): return
        if not self.driver: return
        ctx = ctx or {}
        index = ctx.get("index", 0)
        repeat = ctx.get("repeat", 1)
        extra_s = "-%d" % (index + 1) if repeat > 1 else ""
        base_path = appier.conf("SCREENSHOTS_PATH", ".")
        test_name = util.test_fullname(test)
        if not os.path.exists(base_path): os.makedirs(base_path)
        screen_path = os.path.join(base_path, test_name + extra_s + ".png")
        screen_path = os.path.abspath(screen_path)
        screen_path = os.path.normpath(screen_path)
        self.driver.screenshot(screen_path)
