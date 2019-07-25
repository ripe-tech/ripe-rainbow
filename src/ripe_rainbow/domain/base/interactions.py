#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class InteractionsPart(parts.Part):

    def get_page(self, url, params = [], fragment = ""):
        """
        Navigates to a certain URL with given params.

        :type url: str
        :param url: The URL to navigate to.
        :type params: list
        :param params: A list of (key, values) tuples representing
        the query parameters.
        :type fragment: str
        :param fragment: The fragment string.
        :rtype bool
        :return: 'true' if it was successfully redirected.
        """
        params_s = []

        for (key, value) in params:
            key_q = appier.util.quote(key)
            for _value in value:
                value_q = appier.util.quote(_value)
                param = key_q + "=" + value_q
                params_s.append(param)

        joined_params = "&".join(params_s) if params_s else ""

        joined_url = url
        if joined_params: joined_url += "?" + joined_params
        if fragment: joined_url += "#" + fragment

        self.driver.get(joined_url)

        return self.waits.redirected_to(joined_url)

    def write_text(self, selector, text):
        """
        Writes the text in the given element, this means having
        it typed like in a physical keyboard.

        :type selector: String
        :param selector: The selector for the element to write the text in.
        :type text: String
        :param text: The text to write "using the keyboard".
        :rtype: Element
        :return: The element with the text changed.
        """

        # waits for the element to be available at the DOM
        element = self.waits.element(selector)

        # waits until a valid text change in the element is possible, this
        # overcomes limitations with non interactable elements
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.write_text, element, text),
            "Element '%s' found but never became writable" % selector
        )

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
        :rtype: Element
        :return: The element with the key pressed.
        """

        # waits for the element to be available at the DOM
        element = self.waits.element(selector)

        # waits until a valid key stroke in the element is possible, this
        # overcomes limitations with non interactable elements
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.press_key, element, key),
            "Element '%s' found but never became interactable" % selector
        )

    def press_enter(self, selector):
        """
        Presses the enter key on a certain element, pressed like having
        the proper enter key pressed.

        :type selector: String
        :param selector: The selector for the element to focus when
        pressing enter.
        :rtype: Element
        :return: The element with the enter key pressed.
        """

        # waits for the element to be available at the DOM
        element = self.waits.element(selector)

        # waits until a valid key stroke in the element is possible, this
        # overcomes limitations with non interactable elements
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.press_enter, element),
            "Element '%s' found but never became interactable" % selector
        )

    def click_when_possible(self, selector, condition = None):
        """
        Clicks an element when possible, which happens when that element is both
        visible and "clickable".

        :type selector: String
        :param selector: The selector for the element to click.
        :type condition: Function
        :param condition: The filter the selected element must pass to be "clickable".
        :rtype: Element
        :return: The clicked element if there's any otherwise an invalid value.
        """

        # waits for the element to be available at the DOM
        element = self.waits.element(selector, condition = condition)

        # waits until the try click operation is possible meaning that a
        # proper click has been "done" by the driver
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.click, element),
            "Element '%s' found but never became clickable" % selector
        )
