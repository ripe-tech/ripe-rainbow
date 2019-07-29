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
            lambda d: self.assertions.at_url(
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

    def all(self, selector, condition, timeout = None):
        return self.until(
            lambda d: self.assertions.all(selector, condition),
            message = "Elements for '%s' don't match the condition" % selector,
            timeout = timeout
        )

    def element(self, selector, condition = None, timeout = None):
        return self.until(
            lambda d: self.assertions.exists(selector, condition = condition),
            message = "Element '%s' not found" % selector,
            timeout = timeout
        )

    def elements(self, selector, condition = None, timeout = None):
        return self.until(
            lambda d: self.assertions.exists_multiple(selector, condition = condition),
            message = "Elements '%s' not found" % selector,
            timeout = timeout
        )

    def text(self, selector, text, timeout = None):
        return self.until(
            lambda d: self.assertions.has_text(selector, text),
            message = "Element '%s' with text '%s' not found" % (selector, text),
            timeout = timeout
        )

    def is_visible(self, selector, condition = None, timeout = None):
        return self.until(
            lambda d: self.assertions.is_visible(selector, condition = condition),
            message = "Element '%s' is not visible" % selector,
            timeout = timeout
        )

    def is_not_visible(self, selector, condition = None, timeout = None):
        return self.until(
            lambda d: self.assertions.is_not_visible(selector, condition = condition),
            message = "Element '%s' is visible" % selector,
            timeout = timeout
        )
