#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import appier

from .. import parts

class AssertionsPart(parts.Part):

    def at_url(self, url, params = None, fragment = None, starts_with = False):
        # retrieves the current URL as a string from the underlying
        # driver so that it can be verified
        current_url = self.driver.current_url

        return self.same_url(
            current_url,
            url,
            params = params,
            fragment = fragment,
            starts_with = starts_with
        )

    def same_url(self, actual_url, expected, params = None, strict_params = False, fragment = None, starts_with = False):
        """
        Verifies if 'actual' is the same as 'expected', including its query parameters and fragment.

        :type actual_url: str
        :param actual_url: The URL whose correctness is being checked.
        :type expected: Union[str, list, tuple, regex]
        :param expected: The possible URLs. If 'actual' is the same as one of these,
        or matches one of the regex, then it satisfies the assertion.
        :type strict_params: bool
        :param strict_params: If 'true', the URL must exactly have 'params',
        otherwise it can only contain 'params'.
        :type params: dict[str, str]
        :param params: The URL must have exactly these parameters.
        :param fragment: The URL must have this exact fragment.
        :type starts_with: bool
        :param starts_with: Whether to use a 'starts with'
        :rtype bool
        :return: 'True' if it satisfies the assertion.
        """

        if params: params = {
            appier.legacy.u(key): appier.legacy.u(value) if isinstance(value, (list, tuple)) else [appier.legacy.u(value)]
            for (key, value) in appier.legacy.iteritems(params)
        }

        # parses the actual URL and reconstructs it with just the
        # base scheme and the URL path
        actual_url_p = appier.legacy.urlparse(actual_url)
        actual_url_params = appier.http._params(actual_url_p.query)
        actual_url_base = appier.legacy.u(actual_url_p.scheme + "://" + actual_url_p.netloc + actual_url_p.path)

        # in case the provided URL is not a sequence converts it into
        # one so that it can be used in the underlying algorithm
        if not isinstance(expected, (list, tuple)): expected = (expected,)

        # iterates over the complete set of URLs to be tested and sees
        # if at least one of them validates as a prefix
        for _expected in expected:
            if starts_with and not actual_url.startswith(_expected): continue
            elif hasattr(_expected, "match") and not _expected.match(actual_url): continue
            else:
                _url_p = appier.legacy.urlparse(_expected)
                _url_base = appier.legacy.u(_url_p.scheme + "://" + _url_p.netloc + _url_p.path)
                if not _url_base == actual_url_base: continue

            # runs the extra set of verification (parameters and fragment) in
            # case they have been requested (proper parameters set)
            if params:
                # if strict checks if the actual parameters exactly match the expected ones
                if strict_params and not actual_url_params == params: continue
                # otherwise check that the actual parameters are a superset of the expected ones
                elif self._legacy_items(actual_url_params) < self._legacy_items(params): continue

            if not fragment == None and not actual_url_p.fragment == fragment: continue

            # returns a valid value as the current URL in iteration complies
            # with the complete set of items for acceptance criteria
            return True

        self.breadcrumbs.debug("Actual URL is '%s' and not '%s'" % (actual_url, ",".join(expected)))

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

    def _legacy_items(self, dictionary):
        python3 = sys.version_info[0] >= 3

        if python3: return dictionary.items()
        return dictionary.viewitems()
