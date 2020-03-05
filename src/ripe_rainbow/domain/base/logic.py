#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class LogicPart(parts.Part):

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

    def has_text(self, element, selector, text, safe = True):
        text = appier.legacy.u(text)

        if not element: return None

        # tries to retrieve the text (value) from the element taking into consideration
        # the kind of element that is being validation
        if element.tag_name == "input":
            # retrieves the DOM value attribute for the element as the
            # textual representation for it
            element_text = element.get_attribute("value")
        else:
            # scroll the current viewport to the element selection so that it's
            # safer to verify the text content of it, the underlying driver under
            # some conditions requires viewport visibility to verify the text
            if safe: self.driver.safe(self.driver.scroll_to, element)

            # retrieves the visual textual representation of the element as the
            # value for the element text, this value is only guaranteed to be valid
            # in case the element is visible on the viewport (display not none and
            # opacity greater than zero)
            element_text = element.text

        if not element_text == text:
            self.breadcrumbs.debug("Element '%s' found but has text '%s' instead of '%s'" % (
                selector,
                element_text,
                text
            ))

            return None

        self.breadcrumbs.debug("Found element '%s' with text '%s'" % (
            selector,
            text
        ))

        return element

    def get(self, selector, condition = None):
        # tries to retrieve the complete set of elements that match
        # the provided selector and fulfill the condition
        matching = self.find(selector, condition = condition)

        # verifies if there are too many elements selected and raises
        # a warning as that probably indicated that the selector is broad
        if len(matching) > 1:
            self.breadcrumbs.warning(
                "Found more than one element for selector '%s', "
                "more specific selector is required" % selector
            )

        # returns the properly selected element in case there are valid
        # matches or an invalid value otherwise
        return matching[0] if len(matching) > 0 else None

    def find(self, selector, condition = None):
        # determines if there's a valid condition provided and if that's
        # not the case sets the default condition value
        has_condition = True if condition else False
        if not condition: condition = lambda e, s: True

        # runs the selection operation using the underlying driver
        elements = self.driver.safe(self.driver.find_elements_by_css_selector, selector)

        # in case no elements match the provided selector then returns the
        # empty sequence immediately
        if not elements or len(elements) == 0:
            self.breadcrumbs.debug("Could not find elements with '%s'" % selector)
            return []

        # runs the filtering operation so that only the elements that match
        # the provided condition are selected (requires at least one to pass)
        elements = [element for element in elements if condition(element, selector)]

        # iterates over the complete set of selected elements to monkey patch
        # them with the extra domain specific symbols to allow extra information
        # and interaction to be accessible at an element level
        for element in elements:
            self._patch_element(
                element,
                selector = selector,
                condition = condition
            )

        # prints the proper debug message for diagnostics taking into account
        # the kind of selection that has been performed in the elements
        if len(elements) == 0:
            self.breadcrumbs.debug("Found elements with '%s' but none matches the condition" % selector)
        elif has_condition:
            self.breadcrumbs.debug("Found elements with '%s' that match the condition" % selector)
        else:
            self.breadcrumbs.debug("Found elements with '%s'" % selector)

        # returns the complete set of element that exist in the current context
        # and that match the requested condition
        return elements

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

    def _patch_element(self, element, selector = None, condition = None):
        def _is_same():
            _element = self.get(element._selector, condition = element._condition)
            return _element.id == element.id

        def _ensure_same(message = None):
            if element._is_same(): return
            message = message or "Element (%s) is not the same" % element._text()
            raise appier.OperationalError(message = message)

        def _text():
            description_s = " %s" % element._condition_description if element._condition_description else ""
            return "%s%s" % (element._selector, description_s)

        def _attr(key, value):
            if value: return self.driver.instance.execute_script("arguments[0].%s = \"%s\";" % (key, value), element)
            return self.driver.instance.execute_script("return arguments[0].%s;" % key, element)

        def _highlight():
            self.driver.highlight(element)

        def _lowlight():
            self.driver.lowlight(element)

        element._selector = selector
        element._condition = condition
        element._condition_description = getattr(condition, "_description", None)

        element._is_same = _is_same
        element._ensure_same = _ensure_same
        element._text = _text
        element._attr = _attr
        element._highlight = _highlight
        element._lowlight = _lowlight
