#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.common.exceptions import NoSuchElementException
except ImportError: NoSuchElementException = None

class AssertionsPart(parts.Part):

    def at_url(self, url):
        current_url = self.driver.current_url

        if url in current_url:
            return True

        self.logger.debug("Current page is '%s' and not '%s'." % (current_url, url))

        return False

    def has_text(self, selector, text):
        selector = appier.legacy.u(selector)
        text = appier.legacy.u(text)

        element = self.exists(selector)

        if element and not element.text == text:
            self.logger.debug("Element '%s' found but has text '%s' instead of '%s'." % (
                selector,
                element.text,
                text
            ))

            return None

        self.logger.debug("Found element '%s' with text '%s'." % (
            selector,
            text
        ))

        return element

    def exists_multiple(self, selector, condition = None):
        elements = self.driver.find_elements_by_css_selector(selector)

        if len(elements) == 0:
            self.logger.debug("Could not find elements with '%s'." % selector)

            return elements

        matching_elements = [element for element in elements if condition(element)] if condition else elements

        if len(matching_elements) == 0:
            self.logger.debug("Found elements with '%s' but none matches the condition." % selector)
        elif condition:
            self.logger.debug("Found elements with '%s' that match the condition." % selector)
        else:
            self.logger.debug("Found elements with '%s'." % selector)

        return matching_elements

    def exists(self, selector):
        try:
            element = self.driver.find_element_by_css_selector(selector)

            self.logger.debug("Found element with '%s'." % selector)

            return element
        except NoSuchElementException:
            self.logger.debug("Could not find element with '%s'." % selector)

            return None

    def is_visible(self, selector):
        element = self.exists(selector)
        return element.is_displayed()
