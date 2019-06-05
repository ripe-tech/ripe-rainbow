#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import ElementClickInterceptedException, ElementNotVisibleException

from .. import parts

class InteractionsPart(parts.Part):

    def __init__(self, driver, timeout, logger, waits):
        self.driver = driver
        self.timeout = timeout
        self.logger = logger
        self.waits = waits

    def try_click(self, element):
        try:
            element.click()
            return element
        except (ElementClickInterceptedException, ElementNotVisibleException) as exception:
            self.logger.debug("Element is not \"clickable\" because: %s" % exception)
            return None

    def click_when_possible(self, selector):
        element = self.waits.element(selector)
        return self.waits.until(
            lambda _: self.try_click(element),
            "Element '%s' found but never became clickable" % selector
        )
