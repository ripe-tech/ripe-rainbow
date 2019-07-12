#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

class InteractionsPart(parts.Part):

    def try_click(self, element, scroll = True, scroll_sleep = None):
        return self.driver.click(
            element,
            scroll = scroll,
            scroll_sleep = scroll_sleep
        )

    def click_when_possible(
        self,
        selector,
        condition = None,
        scroll = True,
        scroll_sleep = None
    ):
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
        :type scroll_sleep: int
        :param scroll_sleep: The number of seconds to wait after scrolling, which is
        useful when the scroll is smooth and not immediate.
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
            lambda d: self.try_click(element, scroll = scroll, scroll_sleep = scroll_sleep),
            "Element '%s' found but never became clickable" % selector
        )
