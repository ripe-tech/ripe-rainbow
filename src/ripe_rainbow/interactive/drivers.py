#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import appier

class InteractiveDriver(object):

    def start(self):
        pass

    def stop(self):
        pass

    def get(self, url):
        raise appier.NotImplementedError()

    def find_element(self, selector):
        raise appier.NotImplementedError()

class SeleniumDriver(InteractiveDriver):

    def __init__(self):
        InteractiveDriver.__init__(self)
        self.instance = None
        self.headless = appier.conf("SEL_HEADLESS", False, cast = bool)

    def start(self):
        InteractiveDriver.start(self)
        import selenium.webdriver
        self.instance = selenium.webdriver.Chrome(
            chrome_options = self._selenium_options()
        )

    def stop(self):
        self.instance = None
        InteractiveDriver.stop(self)

    def get(self, url):
        return self.instance.get(url)

    def find_element(self, selector):
        return self.instance.find_element_by_css_selector(selector)

    def find_element_by_css_selector(self, selector):
        return self.find_element(selector)

    def _selenium_options(self):
        import selenium.webdriver

        # crates the base object for the options to be used by
        # the Google Chrome browser
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
