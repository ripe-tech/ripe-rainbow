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

    def try_click(self, element):
        try:
            element.click()
            return element
        except (
            ElementClickInterceptedException,
            ElementNotVisibleException,
            WebDriverException
        ) as exception:
            self.logger.debug("Element is not \"clickable\" because: %s" % exception)
            return None

    def click_when_possible(self, selector):
        element = self.waits.element(selector)
        return self.waits.until(
            lambda d: self.try_click(element),
            "Element '%s' found but never became clickable" % selector
        )
