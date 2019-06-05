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

    @property
    def current_url(self):
        raise appier.NotImplementedError()

class SeleniumDriver(InteractiveDriver):

    def __init__(self):
        InteractiveDriver.__init__(self)
        self.headless = appier.conf("SEL_HEADLESS", False, cast = bool)

    def get(self, url):
        return self.instance.get(url)

    def find_element(self, selector):
        return self.instance.find_element_by_css_selector(selector)

    def find_element_by_css_selector(self, selector):
        return self.find_element(selector)

    @property
    def current_url(self):
        return self.instance.current_url

    @property
    def instance(self):
        cls = self.__class__
        if hasattr(cls, "_instance"): return cls._instance
        import selenium.webdriver
        cls._instance = selenium.webdriver.Chrome(
            chrome_options = self._selenium_options()
        )
        return cls._instance

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
