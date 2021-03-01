#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import appier

from .. import parts

class InteractionsPart(parts.Part):

    def goto_url(self, url, redirect_url = None, params = [], fragment = "", wait = True):
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
        :type redirect_url: String
        :param redirect_url: The target URL of the redirection (if different
        from the target one) to be used in the wait verification.
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

        return self.waits.redirected_to(redirect_url or url)

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

        # waits until the element is visible for the selector and then
        # retrieves the reference to it to be able to write text
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

        # waits until the element is visible for the selector and then
        # retrieves the reference to it to be able to press the key
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

        # waits until the element is visible for the selector and then
        # retrieves the reference to it to be able to press enter
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

    def set_file(self, selector, path):
        """
        Sets a file to a file input element when possible, which happens
        when that element exists.

        This operation only sets the file association in the target element
        the upload/send operation should be triggered by the containing
        form element.

        :type selector: String
        :param selector: The selector for the file input element to set
        the file to, the file will only be sent once the form where the
        element is contained is submitted.
        :type path: String
        :param path: The path to the file being sent in the local filesystem.
        :rtype: Element
        :return: The file input element if there's any otherwise an invalid value.
        """

        # normalizes the path (that can be relative) so that it can
        # be safely used by the de underlying element changing operations
        path = os.path.abspath(path)
        path = os.path.normpath(path)

        # waits until the try set operation is possible meaning that
        # the target element exists and the upload was successful
        return self.waits.until(
            lambda d: self._set_file(selector, path),
            "Could not set '%s' to '%s'" % (path, selector)
        )

    def highlight(self, selector, text = None):
        # waits until the element is visible for the selector and then
        # retrieves the reference to it to be able to press enter
        element = self.waits.visible(selector, text = text)

        # waits until the highlight operation is possible for the element
        # that has just been ensured as visible
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.highlight, element),
            "Element '%s' found but was not possible to highlight it" % selector
        )

    def lowlight(self, selector, text = None):
        # waits until the element is visible for the selector and then
        # retrieves the reference to it to be able to press enter
        element = self.waits.visible(selector, text = text)

        # waits until the lowlight operation is possible for the element
        # that has just been ensured as visible
        return self.waits.until(
            lambda d: self.driver.safe(self.driver.lowlight, element),
            "Element '%s' found but was not possible to lowlight it" % selector
        )

    def switch_tab(self, tab):
        return self.driver.switch_tab(tab)

    def switch_context(self, name = "native", index = 0):
        self.waits.until(
            lambda d: self.driver.count_context(name) > index,
            "Expecting the number of contexts to be at least '%d' but is '%d'" % (
                index,
                self.driver.count_context(name)
            )
        )
        return self.driver.switch_context(name, dict(index = index))

    def close_tab(self, tab = None):
        return self.driver.close_tab(tab)

    @property
    def url(self):
        return self.driver.current_url

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

        element = self.waits._get_element(
            selector,
            text = text,
            displayed = False,
            visible = False
        )
        if not element: return None
        return self.driver.safe(self.driver.click, element)

    def _set_file(self, selector, path):
        """
        Inner method that tries to set the file given by path to
        the file input element defined by the selector.

        This method is ready to be used within a waits environment so that
        proper repetition may happen.

        :type selector: String
        :param selector: The selector for the file input element to set
        the file to.
        :type path: String
        :param path: The local filesystem path to the file being sent.
        :rtype: Element
        :return: The file input element if there's any otherwise an invalid value.
        """

        element = self.logic.get(selector)
        if not element: return None
        return self.driver.safe(self.driver.write_text, element, path, False)
