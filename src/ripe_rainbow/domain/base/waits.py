#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

try: from selenium.webdriver.support.ui import WebDriverWait
except ImportError: WebDriverWait = None

try: from selenium.common.exceptions import StaleElementReferenceException
except ImportError: StaleElementReferenceException = None

class WaitsPart(parts.Part):

    def __init__(self, owner):
        parts.Part.__init__(self, owner)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def wrap_method(self, method, *args):
        """
        Wraps the method being waited on to tolerate some exceptions since
        in most cases these are transitory conditions that shouldn't break
        the test.

        :type method: Function
        :param method: The method being ran.
        :type args: List
        :param args: The arguments provided to the method.
        :rtype Function
        :return: The method wrapped on a try-catch for StaleElementReferenceException.
        """

        try:
            return method(*args)
        except (StaleElementReferenceException, AssertionError) as e:
            self.logger.debug("Got exception while waiting: %s" % e)
            return None

    def until(self, method, message = None):
        return self.wait.until(
            lambda *args: self.wrap_method(method, *args),
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
