#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class AssertionsPart(parts.Part):

    def at_url(
        self,
        url,
        params = None,
        fragment = None,
        starts_with = False,
        strict = False
    ):
        # retrieves the current URL as a string from the underlying
        # driver so that it can be verified
        current_url = self.driver.current_url

        # runs the URL verification taking into account the URL currently
        # set in the driver (the interactive browser)
        return self.match_url(
            current_url,
            url,
            params = params,
            fragment = fragment,
            starts_with = starts_with,
            strict = strict
        )

    def match_url(
        self,
        url,
        expected,
        params = None,
        fragment = None,
        starts_with = False,
        strict = False
    ):
        # runs the normalization process for the provided parameters,
        # so that they can be readily compared with the parsed ones
        params = self._normalize_params(params)

        # parses the current URL in the browser and reconstructs it with just
        # the base scheme and the URL path
        url_p = appier.legacy.urlparse(url)
        url_params = appier.http._params(url_p.query)
        url_base = url_p.scheme + "://" + url_p.netloc + url_p.path

        # in case the provided URL is not a sequence converts it into
        # one so that it can be used in the underlying algorithm
        if not isinstance(expected, (list, tuple)): expected = (expected,)

        # iterates over the complete set of (expected) URLs to be tested and
        # sees if at least one of them validates against the provided base URL
        for _url in expected:
            # in case the starts with mode is active verifies that the current
            # URL starts with the current expected in iteration
            if starts_with and not url.startswith(_url): continue

            # otherwise tries to run the regex match operation (by asserting
            # that the match method is present)
            elif hasattr(_url, "match") and not _url.match(url): continue

            # otherwise runs the "default" net location and path based verification
            # so that the "initial" part of the URL is validated (no query of fragment)
            else:
                _url_p = appier.legacy.urlparse(_url)
                _url_base = _url_p.scheme + "://" + _url_p.netloc + _url_p.path
                if not _url_base == url_base: continue

            # runs the extra set of verification (parameters and fragment) in
            # case they have been requested (proper parameters set)
            if not params == None and not\
                self._compare_params(url_params, params, strict = strict): continue
            if not fragment == None and not url_p.fragment == fragment: continue

            # returns a valid value as the current URL in iteration complies
            # with the complete set of items for acceptance criteria
            return True

        # prints a debug message on the breadcrumbs logger indicating that there's
        # a missmatch in the verification of the URL
        self.breadcrumbs.debug("Provided URL is '%s' and not '%s'" % (url, expected))

        # returns the invalid value as none of the expected URL was able to be validated
        # against the provided URL
        return False

    def has_text(self, selector, text, ensure = False):
        selector = appier.legacy.u(selector)
        text = appier.legacy.u(text)

        element = self.exists(selector)

        if element:
            # in case the ensure flag is set makes sure that the element is visible
            # from an interactable point of view
            if ensure: self.driver.safe(self.driver.ensure_visible, element)

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

    def all(self, selector, condition):
        elements = self.driver.safe(self.driver.find_elements, selector)
        matching = [element for element in elements if condition(element)]

        if not len(matching) == len(elements):
            self.breadcrumbs.debug(
                "Some elements for the selector '%s' don't fulfill the expected condition" % selector
            )
            return None

        return matching

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
        # the provided condition are selected (requires at least one to pass)
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

    def _normalize_params(self, params):
        if not params: return params
        return dict((key, value if isinstance(value, (list, tuple)) else [value]) for\
            key, value in appier.legacy.iteritems(params))

    def _compare_params(self, first, second, strict = False):
        if strict: return first == second
        for key in second:
            if not key in first: return False
            if not first[key] == second[key]: return False
        return True
