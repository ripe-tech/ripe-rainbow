#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

class RetailPart(parts.Part):

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

    def select_size(self, scale, size):
        """
        Opens the size selection window, selects the proper scale and size and
        applies that configuration by clicking 'Apply' and closing the window.

        :type scale: String
        :param scale: The scale that is going to be picked.
        :type size: String
        :param size: The size (in provided scale) to be picked.
        """

        self.interactions.click_when_possible(".size:not(.disabled) .button-size")

        self.interactions.click_when_possible(
            ".size .button-scale",
            condition = lambda element: element.text == str(scale)
        )
        self.waits.element(
            ".size .button-scale.active",
            condition = lambda element: element.text == str(scale)
        )

        self.interactions.click_when_possible(
            ".size .button-size",
            condition = lambda element: element.text == str(size)
        )

        self.interactions.click_when_possible(".size .button.button-primary.button-apply")
        self.waits.is_not_visible(".size .modal-container")

    def set_part(self, brand, model, part, material, color):
        """
        Makes a change to the customization of a part and checks that the pages
        mutates correctly, picking the right active parts, materials and colors,
        as well as properly switching the swatches.

        :type brand: String
        :param brand: The brand of the model.
        :type model: String
        :param model: The model being customized.
        :type part: String
        :param part: The part being changed.
        :type material: String
        :param material: The material to use for the part.
        :type color: String
        :param color: The color to use for the part.
        """

        self.interactions.click_when_possible(".pickers .button-part", condition = lambda e: e.text == part.upper())
        self.interactions.click_when_possible(".pickers .button-color", condition = lambda e: e.text == color.capitalize())

        self.waits.text(".button-part.active", part.upper())
        self.waits.until(
            lambda d: self.swatch_is_correct(".pickers .button-part.active .swatch > img", brand, model, material, color),
            "Part swatch didn't have the expected image."
        )

        self.waits.text(".button-material.active", material.upper())

        self.waits.text(".button-color.active", color.capitalize())
        self.waits.until(
            lambda d: self.assert_swatch(".pickers .button-color.active .swatch > img", brand, model, material, color),
            "Color swatch didn't have the expected image."
        )

    def assert_swatch(self, selector, brand, model, material, color):
        """
        Checks that the img element identified by the selector points to the correct swatch.

        :param selector: The selector for the img.
        :param brand: The brand of the swatch.
        :param model: The model of the swatch.
        :param material: The material the swatch should represent.
        :param color: The color being shown in the shown.
        :return: Nothing.
        """

        element = self.waits.element(selector)
        src = element.get_attribute("src")
        expected_params = ["brand=%s" % brand, "model=%s" % model, "material=%s" % material, "color=%s" % color]

        is_correct = all(expected_param in src for expected_param in expected_params)

        if not is_correct:
            raise AssertionError("Expected '%s' (src of '%s') to contain '%s'." % (src, selector, expected_params))

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-retail-test.platforme.com")
        return appier.conf("RETAIL_URL", base_url)

    @property
    def login_url(self):
        return "%s/login" % self.base_url

    @property
    def logout_url(self):
        return "%s/logout" % self.base_url
