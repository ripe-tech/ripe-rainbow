#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

class InteractionsPart(parts.Part):

    def try_click(self, element, focus = True):
        return self.driver.click(element, focus = focus)

    def click_when_possible(self, selector, condition = None):
        """
        Clicks an element when possible, which happens when that element is both
        visible and clickable.

        :type selector: String
        :param selector: The selector for the element to click.
        :type condition: Function
        :param condition: The filter the selected element must pass to be clickable.
        :rtype Element
        :return The clicked element if there's any otherwise an invalid value.
        """

        element = self.waits.element(selector, condition = condition)
        self.driver.scroll_to(element)

        element = self.waits.is_visible(selector, condition = condition)

        return self.waits.until(
            lambda d: self.try_click(element),
            "Element '%s' found but never became clickable" % selector
        )
