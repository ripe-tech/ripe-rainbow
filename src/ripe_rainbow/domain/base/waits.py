#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

class WaitsPart(parts.Part):

    def until(self, method, message = None, timeout = None):
        return self.driver.wrap_outer(
            lambda: self.driver._wait(timeout = timeout).until(
                lambda *args: self.driver.wrap_inner(method, *args),
                message = message
            )
        )

    def redirected_to(
        self,
        url,
        params = None,
        fragment = None,
        starts_with = False,
        timeout = None
    ):
        return self.until(
            lambda d: self.logic.at_url(
                url,
                params = params,
                fragment = fragment,
                starts_with = starts_with
            ),
            message = "Expecting the page to be '%s' but is '%s'" % (
                url,
                self.driver.current_url
            ),
            timeout = timeout
        )

    def visible(self, selector, text = None, timeout = None, ensure = True):
        return self.until(
            lambda d: self._ensure_element(selector, text = text, timeout = timeout, ensure = ensure),
            message = "Element '%s' not found or not visible" % selector,
            timeout = timeout
        )

    def not_visible(self, selector, timeout = None):
        return self.until(
            lambda d: not self.logic.get(selector, condition = lambda e, s: e.is_displayed()),
            message = "Element '%s' is visible" % selector,
            timeout = timeout
        )

    def _ensure_element(self, selector, text = None, timeout = None, ensure = True):
        if text: condition = lambda e, s: self.driver.scroll_to(e) and self.logic.has_text(e, s, text)
        else: condition = None
        element = self.logic.get(selector, condition = condition)
        if not element: return None
        if ensure: self.driver.ensure_visible(element, timeout = timeout)
        return element
