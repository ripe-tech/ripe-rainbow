#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

try: from selenium.webdriver.support.ui import WebDriverWait
except ImportError: WebDriverWait = None

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
           lambda d: self.assertions.at_url(url),
            message = "Expecting the page to be '%s' but is '%s'" % (
                url,
                self.driver.current_url
            )
        )

    def element(self, selector, condition = None):
        return self.until(
            lambda d: self.assertions.exists(selector, condition = condition),
            "Element '%s' not found" % selector
        )

    def elements(self, selector, condition = None):
        return self.until(
            lambda d: self.assertions.exists_multiple(selector, condition = condition),
            "Elements '%s' not found" % selector
        )

    def text(self, selector, text):
        return self.until(
            lambda d: self.assertions.has_text(selector, text),
            "Element '%s' with text '%s' not found" % (selector, text)
        )

    def is_visible(self, selector):
        return self.until(
            lambda d: self.assertions.is_visible(selector),
            "Element '%s' is not visible" % selector
        )

    def is_not_visible(self, selector):
        return self.until(
            lambda d: not self.assertions.is_visible(selector),
            "Element '%s' is visible" % selector
        )
