#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

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

    def failed(self, test, exception):
        test_cases.TestCase.failed(self, test, exception)
        self._screenshot(test)

    def load_driver(self, start = True):
        driver_s = appier.conf("DRIVER", "selenium")
        driver_s = self.options.get("driver", driver_s)
        driver = getattr(drivers, driver_s.capitalize() + "Driver")(self)
        if start: driver.start()
        return driver

    def _screenshot(self, test):
        if not appier.conf("SCREENSHOTS", False): return
        if not self.driver: return
        base_path = appier.conf("SCREENSHOTS_PATH", ".")
        test_name = util.test_fullname(test)
        if not os.path.exists(base_path): os.makedirs(base_path)
        screen_path = os.path.join(base_path, test_name + ".png")
        screen_path = os.path.abspath(screen_path)
        screen_path = os.path.normpath(screen_path)
        self.driver.screenshot(screen_path)
