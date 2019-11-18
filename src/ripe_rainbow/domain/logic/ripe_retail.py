#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeRetailPart(parts.Part):

    def login(self, username, password):
        self.driver.get(self.login_url)

        form = self.driver.find_element(".form")
        username_input = form.find_element_by_name("username")
        self.driver.write_text(username_input, username)
        password_input = form.find_element_by_name("password")
        self.driver.write_text(password_input, password)
        self.driver.press_enter(password_input)

    def login_wait(self, username, password):
        self.login(username, password)
        self.waits.redirected_to(self.next_url)

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
        :type open: Boolean
        :param open: If the size modal window should be opened before selection.
        """

        if open: self.interactions.click(".size:not(.disabled) .button-size")

        if gender: self.interactions.click(".size .button-gender", text = gender)

        if scale: self.interactions.click(".size .button-scale", text = str(scale))

        self.interactions.click(".size .button-size", text = str(size))

        self.interactions.click(".size .button.button-apply")
        self.waits.not_visible(".size .modal")

    def select_part(self, part):
        self.interactions.click(".pickers .button-part > p", text = part.upper())

    def assert_no_part(self, part, timeout = None):
        condition = lambda e, s: self.driver.scroll_to(e) and self.logic.has_text(e, s, part.upper())

        self.waits.until(
            lambda d: len(self.logic.find(".pickers .button-part > p", condition = condition)) == 0,
            "The selector for the part '%s' didn't disappear" % part,
            timeout = timeout
        )

    def assert_no_material(self, part, material):
        self.select_part(part)
        self.waits.not_visible(".material li[data-material='%s']" % material)
        self.waits.not_visible(".pickers .button-color[data-material='%s']" % material)

    def assert_no_color(self, part, color):
        self.select_part(part)
        self.waits.not_visible(".pickers .button-color[data-color='%s']" % color)

    def set_part(
        self,
        brand,
        model,
        part,
        material,
        color,
        part_text = None,
        material_text = None,
        color_text = None,
        verify = True,
        has_swatch = True
    ):
        """
        Makes a change to the customization of a part and checks that the pages
        mutates correctly, picking the right active parts, materials and colors,
        as well as properly switching the swatches.

        If the text parameters are passed an extra set of assertions are going
        to be performed to validate expected behaviour.

        :type brand: String
        :param brand: The brand of the model being customized.
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
        :type verify: bool
        :param verify: If a final assertion should be performed after the selection
        has been done (to verify the final status).
        :type has_swatch: Boolean
        :param has_swatch: Whether there should be a swatch.
        """

        self.select_part(part)
        self.interactions.click(
            ".pickers .button-color-option[data-material='%s'][data-color='%s']" % (material, color)
        )

        if verify:
            self.assert_part(
                brand,
                model,
                part,
                material,
                color,
                part_text = part_text,
                material_text = material_text,
                color_text = color_text,
                has_swatch = has_swatch
            )

    def assert_part(
        self,
        brand,
        model,
        part,
        material,
        color,
        part_text = None,
        material_text = None,
        color_text = None,
        has_swatch = True
    ):
        """
        Checks that the part pickers have the expected state, meaning that the
        complete set of assertions are properly filled.

        If the text parameters are passed an extra set of assertions are going
        to be performed to validate expected behaviour.

        Notice that this assertion requires the changing of the current visual
        state, in the sense that the part tab is going to be switched to the
        one that is going to be asserted.

        :type brand: String
        :param brand: The brand of the model being customized.
        :type model: String
        :param model: The model being customized.
        :type part: String
        :param part: The technical name of the part being checked.
        :type material: String
        :param material: The technical name of the material used in the part.
        :type color: String
        :param color: The technical name of the color used in the part.
        :type part_text: String
        :param part_text: The expected label for the part.
        :type material_text: String
        :param material_text: The expected label for the material.
        :type color_text: String
        :param color_text: The expected label for the color.
        :type has_swatch: Boolean
        :param has_swatch: Whether there should be a swatch.
        """

        self.interactions.click(".pickers .button-part", text = part.upper())

        if part_text: self.waits.visible(".button-part.active", text = part_text)
        if color_text: self.waits.visible(".button-color-option.active", text = color_text)
        if material_text: self.waits.visible(".button-material.active", text = material_text)

        if has_swatch:
            self.waits.until(
                lambda d: self.core.assert_swatch(
                    ".pickers .button-part.active .swatch > img",
                    brand, model, material, color
                ),
                "Part swatch didn't have the expected image."
            )

            self.waits.until(
                lambda d: self.core.assert_swatch(
                    ".pickers .button-color-option.active .swatch > img",
                    brand, model, material, color
                ),
                "Color swatch didn't have the expected image."
            )

    @property
    def retail_url(self):
        ripe_suffix = appier.conf("RIPE_SUFFIX", None)
        if ripe_suffix: retail_url = "https://ripe-retail-%s.platforme.com" % ripe_suffix
        else: retail_url = "http://localhost:8080"
        retail_url = appier.conf("BASE_URL", retail_url)
        retail_url = appier.conf("RETAIL_URL", retail_url)
        retail_url = appier.conf("RIPE_RETAIL_URL", retail_url)
        return retail_url

    @property
    def username(self):
        username = appier.conf("RETAIL_USERNAME", "root")
        username = appier.conf("RIPE_RETAIL_USERNAME", username)
        return username

    @property
    def password(self):
        password = appier.conf("RETAIL_PASSWORD", "root")
        password = appier.conf("RIPE_RETAIL_PASSWORD", password)
        return password

    @property
    def base_url(self):
        return self.retail_url

    @property
    def api_url(self):
        return "%s/api" % self.retail_url

    @property
    def admin_url(self):
        return "%s/admin" % self.retail_url

    @property
    def admin_api_url(self):
        return "%s/api/admin" % self.retail_url

    @property
    def export_url(self):
        return "%s/export" % self.retail_url

    @property
    def export_api_url(self):
        return "%s/api/export" % self.retail_url

    @property
    def home_url(self):
        return "%s/" % self.retail_url

    @property
    def next_url(self):
        return self.home_url

    @property
    def login_url(self):
        return "%s/login" % self.retail_url

    @property
    def logout_url(self):
        return "%s/logout" % self.retail_url
