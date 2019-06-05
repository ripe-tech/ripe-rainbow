#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import appier

class InteractiveDriver(object):

    def __init__(self, owner):
        self.owner = owner

    def start(self):
        pass

    def stop(self):
        pass

    def get(self, url):
        raise appier.NotImplementedError()

    def find_element(self, selector):
        raise appier.NotImplementedError()

    def find_elements(self, selector):
        raise appier.NotImplementedError()

    def find_by_name(self, name):
        raise appier.NotImplementedError()

    @property
    def current_url(self):
        raise appier.NotImplementedError()

class SeleniumDriver(InteractiveDriver):

    def __init__(self, owner):
        InteractiveDriver.__init__(self, owner)
        self.maximized = appier.conf("SEL_MAXIMIZED", False, cast = bool)
        self.headless = appier.conf("SEL_HEADLESS", False, cast = bool)

    def get(self, url):
        return self.instance.get(url)

    def find_element(self, selector):
        return self.instance.find_element_by_css_selector(selector)

    def find_elements(self, selector):
        return self.instance.find_elements_by_css_selector(selector)

    def find_by_name(self, name):
        return self.instance.find_element_by_name(name)

    def find_element_by_css_selector(self, selector):
        return self.find_element(selector)

    def find_elements_by_css_selector(self, selector):
        return self.find_elements(selector)

    def find_element_by_name(self, name):
        return self.find_by_name(name)

    @property
    def current_url(self):
        return self.instance.current_url

    @property
    def instance(self):
        cls = self.__class__
        if hasattr(cls, "_instance") and cls._instance:
            return cls._instance
        import selenium.webdriver
        cls._instance = selenium.webdriver.Chrome(
            chrome_options = self._selenium_options()
        )
        self.owner.runner.add_on_finish(self._destroy_instance)
        return cls._instance

    def _destroy_instance(self):
        cls = self.__class__
        if not hasattr(cls, "_instance") or not self._instance:
            return
        cls._instance.close()
        cls._instance = None

    def _selenium_options(self):
        import selenium.webdriver

        # crates the base object for the options to be used by
        # the Google Chrome browser
        options = selenium.webdriver.ChromeOptions()

        # adds some of the default arguments to be used for the
        # execution of the Google Chrome instance
        options.add_argument("--disable-extensions")

        # in case the browser should be started maximized, then
        # a new argument is added to the list of options
        if self.maximized:
            options.add_argument("start-maximized")

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

        # returns the options to the calling method as expected
        # by the current infrastructure
        return options
