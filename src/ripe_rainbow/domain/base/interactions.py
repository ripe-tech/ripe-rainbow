#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

class InteractionsPart(parts.Part):

    def try_click(self, element, focus = True):
        return self.driver.click(element, focus = focus)

    def click_when_possible(self, selector, condition = None, scroll = True):
        """
        Clicks an element when possible, which happens when that element is both
        visible and "clickable".

        Optionally the browser viewport is "scrolled" to the visual position
        of the element, enabling proper "clicking".

        :type selector: String
        :param selector: The selector for the element to click.
        :type condition: Function
        :param condition: The filter the selected element must pass to be "clickable".
        :type scroll: bool
        :param scroll: If the browser viewport should be scrolled to the element
        before the click operation is performed.
        :rtype Element
        :return The clicked element if there's any otherwise an invalid value.
        """

        # waits for the element to be available at the DOM and then
        # optionally runs the scroll operation to the element
        element = self.waits.element(selector, condition = condition)
        if scroll: self.driver.scroll_to(element)

        # waits for the proper visibility of the element, should be ensured
        # by having the element "inside" the current browser viewport
        element = self.waits.is_visible(selector, condition = condition)

        # waits until the try click operation is possible meaning that a
        # proper click has been "done" by the driver
        return self.waits.until(
            lambda d: self.try_click(element),
            "Element '%s' found but never became clickable" % selector
        )
