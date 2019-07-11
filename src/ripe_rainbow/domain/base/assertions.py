#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.common.exceptions import NoSuchElementException
except ImportError: NoSuchElementException = None

class AssertionsPart(parts.Part):

    def at_url(self, url):
        current_url = self.driver.current_url

        # in case the current URL of the driver is the expected one
        # returns a valid value immediately
        if url in current_url:
            return True

        self.logger.debug("Current page is '%s' and not '%s'" % (current_url, url))

        return False

    def has_text(self, selector, text):
        selector = appier.legacy.u(selector)
        text = appier.legacy.u(text)

        element = self.exists(selector)

        if element and not element.text == text:
            self.logger.debug("Element '%s' found but has text '%s' instead of '%s'" % (
                selector,
                element.text,
                text
            ))

            return None

        self.logger.debug("Found element '%s' with text '%s'" % (
            selector,
            text
        ))

        return element

    def exists(self, selector, condition = None):
        # tries to retrieve the complete set of elements that match
        # the provided selector and fulfill the condition if there's
        # at least one valid returns it otherwise returns invalid
        matching = self.exists_multiple(selector, condition = condition)
        return matching[0] if len(matching) > 0 else None

    def exists_multiple(self, selector, condition = None):
        # determines if there's a valid condition provided and if that's
        # not the case sets the default condition value
        has_condition = True if condition else False
        if not condition: condition = lambda e: True

        # runs the selection operation using the underlying driver
        elements = self.driver.find_elements_by_css_selector(selector)

        # in case no elements match the provided selector then returns the
        # empty sequence immediately
        if len(elements) == 0:
            self.logger.debug("Could not find elements with '%s'" % selector)
            return elements

        # runs the filtering operation so that only the elements that match
        # the provided condition are selected
        elements = [element for element in elements if condition(element)]

        if len(elements) == 0:
            self.logger.debug("Found elements with '%s' but none matches the condition" % selector)
        elif has_condition:
            self.logger.debug("Found elements with '%s' that match the condition" % selector)
        else:
            self.logger.debug("Found elements with '%s'" % selector)

        # returns the complete set of element that exist in the current context
        # and that match the requested condition
        return elements

    def is_visible(self, selector, condition = None):
        # runs the selector with the requested condition to retrieve a possible
        # element and returns invalid if there's none
        element = self.exists(selector, condition = condition)
        if not element: return None

        # verifies that the element is currently displayed in the screen (visible)
        # and if not returns an invalid value
        return element if element.is_displayed() else None

    def is_not_visible(self, selector, condition = None):
        # runs the selector with the requested condition to retrieve a possible
        # element and returns invalid if there's none
        element = self.exists(selector, condition = condition)
        if not element: return None

        # verifies that the element is not currently displayed in the screen
        # (invisible) and if not returns an invalid value
        return None if element.is_displayed() else element
