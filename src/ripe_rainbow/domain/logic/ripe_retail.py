#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

class RipeRetailPart(parts.Part):

    def login(self, username, password):
        self.driver.get(self.login_url)

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def login_and_redirect(self, username, password):
        self.login(username, password)

        self.waits.redirected_to(self.base_url)

    def select_size(self, size, gender = None, scale = None, open = True):
        """
        Opens the size selection window, selects the proper scale and size and
        applies that configuration by clicking 'Apply' and closing the window.

        Notice that if the "open" flag is unset the window is not opened.

        :type size: String
        :param size: The size to be picked.
        :type gender: String
        :param gender: The gender that is going to be picked.
        :type scale: String
        :param scale: The scale that is going to be picked.
        :type already_open: Boolean
        :param already_open: Whether the size modal is already open.
        """

        if open: self.interactions.click_when_possible(".size:not(.disabled) .button-size")

        if gender:
            self.interactions.click_when_possible(
                ".size .button-gender",
                condition = lambda element: element.text == gender
            )

        if scale:
            self.interactions.click_when_possible(
                ".size .button-scale",
                condition = lambda element: element.text == str(scale)
            )

        self.interactions.click_when_possible(
            ".size .button-size",
            condition = lambda element: element.text == str(size)
        )

        self.interactions.click_when_possible(".size .button.button-primary.button-apply")
        self.waits.is_not_visible(".size .modal")

    def set_part(
        self,
        brand,
        model,
        part,
        material,
        color,
        part_text = None,
        material_text = None,
        color_text = None
    ):
        """
        Makes a change to the customization of a part and checks that the pages
        mutates correctly, picking the right active parts, materials and colors,
        as well as properly switching the swatches.

        If the text parameters are passed an extra set of assertions are going
        to be performed to validate expected behaviour.

        :type brand: String
        :param brand: The brand of the model.
        :type model: String
        :param model: The model being customized.
        :type part: String
        :param part: The technical name of the part being changed.
        :type material: String
        :param material: The technical name of the material to use for the part.
        :type color: String
        :param color: The technical name of the color to use for the part.
        :type part_text: String
        :param part_text: The expected label for the part after clicking.
        :type material_text: String
        :param material_text: The expected label for the material after clicking.
        :type color_text: String
        :param color_text: The expected label for the color after clicking.
        """

        self.interactions.click_when_possible(
            ".pickers .button-part",
            condition = lambda e: e.text == part.upper()
        )
        if part_text: self.waits.text(".button-part.active", part_text)

        self.interactions.click_when_possible(".pickers .button-color[data-color='%s']" % color)

        if color_text: self.waits.text(".button-color.active", color_text)
        if material_text: self.waits.text(".button-material.active", material_text)

        self.waits.until(
            lambda d: self.assert_swatch(
                ".pickers .button-part.active .swatch > img",
                brand, model, material, color
            ),
            "Part swatch didn't have the expected image."
        )
        self.waits.until(
            lambda d: self.assert_swatch(
                ".pickers .button-color.active .swatch > img",
                brand, model, material, color
            ),
            "Color swatch didn't have the expected image."
        )

    def assert_swatch(self, selector, brand, model, material, color):
        """
        Checks that the img element identified by the selector points to the
        correct swatch. The correctness verification is performed by checking
        the "src" attribute of the element.

        This kind of assertion is critical to ensure proper responsiveness of
        the UI in accordance with part selection.

        :type selector: String
        :param selector: The selector for the img.
        :type brand: String
        :param brand: The brand of the swatch.
        :type model: String
        :param model: The model of the swatch.
        :type material: String
        :param material: The material the swatch should represent.
        :type color: String
        :param color: The color being shown in the shown.
        :rtype: Element
        :return: The element with the swatch image.
        """

        element = self.waits.element(selector)
        src = element.get_attribute("src")
        expected_params = [
            "brand=%s" % brand,
            "model=%s" % model,
            "material=%s" % material,
            "color=%s" % color
        ]

        is_correct = all(expected_param in src for expected_param in expected_params)

        if not is_correct:
            raise AssertionError(
                "Expected '%s' (src of '%s') to contain '%s'." %\
                (src, selector, expected_params)
            )

        return element

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-retail-ci.platforme.com")
        base_url = appier.conf("RETAIL_URL", base_url)
        base_url = appier.conf("RIPE_RETAIL_URL", base_url)
        return base_url

    @property
    def login_url(self):
        return "%s/login" % self.base_url

    @property
    def logout_url(self):
        return "%s/logout" % self.base_url
