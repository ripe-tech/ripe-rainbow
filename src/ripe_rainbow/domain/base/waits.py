#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

class WaitsPart(parts.Part):

    def until(self, method, message = None, timeout = None):
        return self.driver.wrap_outer(
            lambda: self.driver._wait(timeout = timeout).until(
                lambda *args: self.driver.wrap_inner(method, *args),
                message = message or "Method was not validated"
            )
        )

    def redirected_to(
        self,
        url,
        params = None,
        fragment = None,
        starts_with = False,
        message = None,
        timeout = None
    ):
        return self.until(
            lambda d: self.logic.at_url(
                url,
                params = params,
                fragment = fragment,
                starts_with = starts_with
            ),
            message = message or "Expecting the page to be '%s' but is '%s'" % (
                url,
                self.driver.current_url
            ),
            timeout = timeout
        )

    def tab_count(self, tab_count, message = None, timeout = None):
        return self.until(
            lambda d: self.driver.tab_count == tab_count,
            message = message or "Expecting the number of browser tabs to be '%s' but is '%s'" % (
                tab_count,
                self.driver.tab_count
            ),
            timeout = timeout
        )

    def visible(
        self,
        selector,
        text = None,
        ensure = True,
        message = None,
        timeout = None
    ):
        return self.until(
            lambda d: self._get_element(
                selector,
                text = text,
                timeout = timeout,
                displayed = True,
                visible = ensure
            ),
            message = message or "Element '%s' not found or not visible" % selector,
            timeout = timeout
        )

    def not_visible(
        self,
        selector,
        text = None,
        ensure = False,
        message = None,
        timeout = None
    ):
        return self.until(
            lambda d: not self._get_element(
                selector,
                text = text,
                timeout = timeout,
                displayed = True,
                visible = ensure
            ),
            message = message or "Element '%s' was found and is visible" % selector,
            timeout = timeout
        )

    def _get_element(
        self,
        selector,
        text = None,
        timeout = None,
        displayed = True,
        visible = True
    ):
        condition = None
        if text:
            condition = self._build_condition(
                lambda e, s: self.logic.has_text(e, s, text),
                description = "text='%s'" % text
            )
        element = self.logic.get(selector, condition = condition)
        if not element: return None
        if displayed:
            try: self.driver.scroll_to(element)
            except Exception: return None
            result = element.is_displayed()
            if not result: return None
        if visible:
            try: self.driver.ensure_visible(element, timeout = timeout)
            except Exception: return None
        return element

    def _build_condition(self, callable, description = None):
        callable._description = description
        return callable
