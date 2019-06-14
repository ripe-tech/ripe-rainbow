#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

try: from selenium.common.exceptions import ElementClickInterceptedException
except ImportError: ElementClickInterceptedException = None

try: from selenium.common.exceptions import ElementNotVisibleException
except ImportError: ElementNotVisibleException = None

try: from selenium.common.exceptions import WebDriverException
except ImportError: WebDriverException = None

class InteractionsPart(parts.Part):

    def try_click(self, element, focus = True):
        try:
            self.driver.click(element, focus = focus)
            return element
        except (
            ElementClickInterceptedException,
            ElementNotVisibleException,
            WebDriverException
        ) as exception:
            self.logger.debug("Element is not \"clickable\" because: %s" % exception)
            return None

    def click_when_possible(self, selector, condition = None):
        element = self.waits.element(selector, condition = condition)
        return self.waits.until(
            lambda d: self.try_click(element),
            "Element '%s' found but never became clickable" % selector
        )
