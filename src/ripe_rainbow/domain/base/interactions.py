#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import parts

class InteractionsPart(parts.Part):

    def write_text(self, selector, text):
        """
        Writes the text in the given element, this means having
        it typed like in a physical keyboard.

        :type selector: String
        :param selector: The selector for the element to write the text in.
        :type text: String
        :param text: The text to write "using the keyboard".
        """

        element = self.waits.element(selector)
        self.driver.safe(self.driver.write_text, element, text)

    def press_key(self, selector, key):
        """
        Presses the provided key on a certain element, pressed like having
        the proper enter key pressed.

        :type selector: String
        :param selector: The selector for the element to focus when
        pressing enter.
        :type key: String
        :param key: The name of the key that is going to be pressed by
        the keyboard, this name is set on an agnostic way.
        """

        element = self.waits.element(selector)
        self.driver.safe(self.driver.press_key, element, key)

    def press_enter(self, selector):
        """
        Presses the enter key on a certain element, pressed like having
        the proper enter key pressed.

        :type selector: String
        :param selector: The selector for the element to focus when
        pressing enter.
        """

        element = self.waits.element(selector)
        self.driver.safe(self.driver.press_enter, element)

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
        if scroll: self.driver.safe(self.driver.scroll_to, element)

        # waits for the proper visibility of the element, should be ensured
        # by having the element "inside" the current browser viewport
        element = self.waits.is_visible(selector, condition = condition)

        # waits until the try click operation is possible meaning that a
        # proper click has been "done" by the driver
        return self.waits.until(
            lambda d: self._try_click(element, scroll = scroll, scroll_sleep = scroll_sleep),
            "Element '%s' found but never became clickable" % selector
        )

    def _try_click(self, element, scroll = True, scroll_sleep = None):
        return self.driver.safe(
            self.driver.click,
            element,
            scroll = scroll,
            scroll_sleep = scroll_sleep
        )
