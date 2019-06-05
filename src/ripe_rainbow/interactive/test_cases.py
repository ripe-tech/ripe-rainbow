#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import drivers

from .. import test_cases

class InteractiveTestCase(test_cases.TestCase):

    def __init__(self, *args, **kwargs):
        test_cases.TestCase.__init__(self, *args, **kwargs)
        self.options = kwargs
        self.driver = None
        self.timeout = appier.conf("TIMEOUT", 60, cast = int)
        self.timeout = self.options.get("timeout", self.timeout)

    def before(self):
        test_cases.TestCase.before(self)
        self.driver = self.load_driver()

    def after(self):
        if self.driver:
            self.driver.stop()
            self.driver = None
        test_cases.TestCase.after(self)

    def load_driver(self, start = True):
        driver_s = appier.conf("DRIVER", "selenium")
        driver_s = self.options.get("driver", driver_s)
        driver = getattr(drivers, driver_s.capitalize() + "Driver")(self)
        if start: driver.start()
        return driver
