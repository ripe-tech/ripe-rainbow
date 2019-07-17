#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class AssertionsPart(parts.Part):

    def at_url(self, url, starts_with = False):
        # retrieves the current URL as a string from the underlying
        # driver so that it can be verified
        current_url = self.driver.current_url

        # parses the current URL in the browser and reconstructs it with just
        # the base scheme and the URL path
        current_url_p = appier.legacy.urlparse(self.driver.current_url)
        current_url_base = current_url_p.scheme + "://" + current_url_p.netloc + current_url_p.path

        # in case the provided URL is not a sequence converts it into
        # one so that it can be used in the underlying algorithm
        if not isinstance(url, (list, tuple)): url = (url,)

        # iterates over the complete set of URLs to be tested and sees
        # if at least one of them validates as a prefix
        for _url in url:
            if starts_with and not current_url.startswith(_url): continue
            elif hasattr(_url, "match") and not _url.match(current_url): continue
            else:
                _url_p = appier.legacy.urlparse(_url)
                _url_base = _url_p.scheme + "://" + _url_p.netloc + _url_p.path
                if not _url_base == current_url_base: continue
            return True

        self.breadcrumbs.debug("Current page is '%s' and not '%s'" % (current_url, ",".join(url)))

        return False

    def has_text(self, selector, text, scroll = True):
        selector = appier.legacy.u(selector)
        text = appier.legacy.u(text)

        element = self.exists(selector)

        if element:
            # scroll the browser to the element, this may change the
            # value of the text found for the element
            if scroll: self.driver.safe(self.driver.scroll_to, element)

            if not element.text == text:
                self.breadcrumbs.debug("Element '%s' found but has text '%s' instead of '%s'" % (
                    selector,
                    element.text,
                    text
                ))

                return None

        self.breadcrumbs.debug("Found element '%s' with text '%s'" % (
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
        elements = self.driver.safe(self.driver.find_elements_by_css_selector, selector)

        # in case no elements match the provided selector then returns the
        # empty sequence immediately
        if len(elements) == 0:
            self.breadcrumbs.debug("Could not find elements with '%s'" % selector)
            return elements

        # runs the filtering operation so that only the elements that match
        # the provided condition are selected
        elements = [element for element in elements if condition(element)]

        if len(elements) == 0:
            self.breadcrumbs.debug("Found elements with '%s' but none matches the condition" % selector)
        elif has_condition:
            self.breadcrumbs.debug("Found elements with '%s' that match the condition" % selector)
        else:
            self.breadcrumbs.debug("Found elements with '%s'" % selector)

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
