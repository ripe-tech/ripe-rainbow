#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class InteractionsPart(parts.Part):

    def goto_url(self, url, params = [], fragment = "", wait = True):
        """
        Navigates to a certain URL with given GET parameters and to
        the request fragment.

        The operation is always going to be performed using a GET
        request as that's the only available request method from
        the browser.

        By default the redirection is waited to verify that the final
        redirection is performed.

        :type url: String
        :param url: The URL to navigate to, this should represent only
        the base URL without GET parameters and fragment.
        :type params: list
        :param params: A list of (key, values) tuples representing
        the GET query parameters to be added to the base URL
        :type fragment: String
        :param fragment: The fragment string to be added to the last part
        of the URL to be built.
        :type wait: bool
        :param wait: If the engine should wait until the browser URL bar
        is set to the destination URL (could pose issues with HTTP redirection).
        :rtype: bool
        :return: The result of the redirection, if it was verified by
        the browser.
        """

        params_s = []

        for (key, value) in params:
            key_q = appier.util.quote(key)
            for _value in value:
                value_q = appier.util.quote(_value)
                param = key_q + "=" + value_q
                params_s.append(param)

        params_s = "&".join(params_s) if params_s else ""

        if params_s: url += "?" + params_s
        if fragment: url += "#" + fragment

        self.driver.get(url)

        if not wait: return

        return self.waits.redirected_to(url)

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

        element = self.waits.visible(selector)

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

        element = self.waits.visible(selector)

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

        element = self.waits.visible(selector)

        # waits until a valid key stroke in the element is possible, this
        # overcomes limitations with non interactable elements
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.press_enter, element),
            "Element '%s' found but never became interactable" % selector
        )

    def click(self, selector, text = None):
        """
        Clicks an element when possible, which happens when that element is both
        visible and "clickable".

        :type selector: String
        :param selector: The selector for the element to click.
        :type text: String
        :param text: The text the selected element must have before being clicked.
        :rtype: Element
        :return: The clicked element if there's any otherwise an invalid value.
        """

        # waits until the try click operation is possible meaning that a
        # proper click has been "done" by the driver
        return self.waits.until(
            lambda d: self._click(selector, text = text),
            "Element '%s' found but never became clickable" % selector
        )

    def _click(self, selector, text = None):
        """
        Inner method that takes the selector and the possible text value of
        a target element and tries to run a click operation in it.

        This method is ready to be used within a waits environment so that
        proper repetition may happen.

        :type selector: String
        :param selector: The selector for the element to click.
        :type text: String
        :param text: The text the selected element must have before being clicked.
        :rtype: Element
        :return: The clicked element if there's any otherwise an invalid value.
        """

        element = self.waits._ensure_element(selector, text = text, ensure = False)
        if not element: return None
        return self.driver.safe(self.driver.click, element)
