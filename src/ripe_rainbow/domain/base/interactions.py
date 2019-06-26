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
        """
        Clicks an element when possible, which happens when that element is both
        visible and clickable.

        :type selector: String
        :param selector: The selector for the element to click.
        :type condition: Function
        :param condition: The filter the selected element mustpass to be clickable.
        :rtype Element
        :return The clicked element if there's any othewise an invalid value.
        """

        element = self.waits.is_visible(selector, condition = condition)
        return self.waits.until(
            lambda d: self.try_click(element),
            "Element '%s' found but never became clickable" % selector
        )
