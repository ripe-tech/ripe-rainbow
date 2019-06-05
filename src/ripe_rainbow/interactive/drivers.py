#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class InteractiveDriver(object):

    def start(self):
        pass

    def stop(self):
        pass

class SeleniumDriver(InteractiveDriver):

    def _selenium_options(self):
        import selenium.webdriver

        options = selenium.webdriver.ChromeOptions()

        # in case the headless mode was selected then an
        # extra argument is added to the set of options
        if self.headless:
            options.add_argument("--headless")

        # fixes issue when running within a docker container
        # since it typically uses /dev/shm shared memory with
        # little space making chrome crash when rendering large pages
        if sys.platform.startswith("linux"):
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
