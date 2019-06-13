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

    def focus(self, element):
        raise appier.NotImplementedError()

    def click(self, element, focus = True):
        raise appier.NotImplementedError()

    @property
    def current_url(self):
        raise appier.NotImplementedError()

class SeleniumDriver(InteractiveDriver):

    def __init__(self, owner):
        InteractiveDriver.__init__(self, owner)
        self.maximized = appier.conf("SEL_MAXIMIZED", False, cast = bool)
        self.headless = appier.conf("SEL_HEADLESS", False, cast = bool)
        self.window_size = appier.conf("SEL_WINDOW_SIZE", "1920x1080")

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

    def focus(self, element):
        from selenium.webdriver.common.action_chains import ActionChains
        actions = ActionChains(self.instance)
        actions.move_to_element(element)
        actions.perform()

    def click(self, element, focus = True):
        from selenium.webdriver.common.action_chains import ActionChains
        if focus:
            actions = ActionChains(self.instance)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()
        else:
            element.click()

    @property
    def current_url(self):
        return self.instance.current_url

    @property
    def instance(self):
        cls = self.__class__
        if hasattr(cls, "_instance") and cls._instance:
            return cls._instance

        import selenium.webdriver

        # creates the underlying instance of the Chomde driver
        # that is going to be used in the concrete exeuction
        cls._instance = selenium.webdriver.Chrome(
            chrome_options = self._selenium_options()
        )

        # in case the browser should be started maximized, then
        # a new argument is added to the list of options
        if self.maximized:
            cls._instance.fullscreen_window()

        # in case the browser should have a specific window size
        # then splits the window size around the specific values
        if self.window_size:
            width, height = (int(value) for value in self.window_size.split("x"))
            cls._instance.set_window_size(width, height)

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
