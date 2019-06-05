#!/usr/bin/python
# -*- coding: utf-8 -*-

try: from selenium.webdriver.support.ui import WebDriverWait
except ImportError: WebDriverWait = None

from .. import parts

class WaitsPart(parts.Part):

    def __init__(self, owner):
        parts.Part.__init__(self, owner)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def until(self, method, message = None):
        return self.wait.until(
            method,
            message = message
        )

    def redirected_to(self, url):
        return self.until(
            lambda _: url in self.driver.current_url,
            message = "Expecting the page to be '%s' but is '%s', even after waiting '%s' seconds." % (
                url,
                self.driver.current_url,
                self.timeout
            )
        )

    def element(self, selector):
        return self.until(
            lambda _: self.assertions.exists(selector),
            "Element '%s' not found after '%s' seconds." % (selector, self.timeout)
        )

    def elements(self, selector, condition = None):
        return self.until(
            lambda _: self.assertions.exists_multiple(selector, condition = condition),
            "Elements '%s' not found after '%s' seconds." % (selector, self.timeout)
        )

    def text(self, selector, text):
        return self.until(
            lambda _: self.assertions.has_text(selector, text),
            "Element '%s' with text '%s' not found after '%s' seconds." % (selector, text, self.timeout)
        )

    def is_not_visible(self, selector):
        return self.until(
            lambda _: not self.assertions.is_visible(selector),
            "Element '%s' is still visible after '%s' seconds." % (selector, self.timeout)
        )
