#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeWhitePart(parts.Part):

    def authorize(self):
        self.id.authorize()

    def select_size(self, size, gender = None, scale = None, open = True, wait_closed = True):
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
        :type wait_closed: Boolean
        :param wait_closed: Whether it should wait for the size modal to be closed,
        not waiting for the closing of the modal should improve performance.
        """

        if open: self.interactions.click(".content .size:not(.disabled) > .button-size")
        if gender: self.interactions.click(".size .button-gender", text = gender)
        if scale: self.interactions.click(".size .button-scale", text = str(scale))

        self.interactions.click(".size .sizes .button-size", text = str(size))
        self.interactions.click(".content .size .button.button-apply")
        if wait_closed: self.waits.not_visible(".content .size .modal")

    def select_size_mobile(self, size, gender = None, scale = None, wait_closed = True):
        """
        Opens the size selection window, selects the proper scale and size and
        applies that configuration by clicking 'Apply' and closing the window.

        Notice that if the "open" flag is unset the window is not opened.

        This method is aimed at the mobile version of the size selector.

        :type size: String
        :param size: The size to be picked.
        :type gender: String
        :param gender: The gender that is going to be picked.
        :type scale: String
        :param scale: The scale that is going to be picked.
        :type open: Boolean
        :param open: If the size modal window should be opened before selection.
        :type wait_closed: Boolean
        :param wait_closed: Whether it should wait for the size modal to be closed,
        not waiting for the closing of the modal should improve performance.
        """

        if gender: self.interactions.click(".size .button-gender", text = gender)
        if scale: self.interactions.click(".size .button-scale", text = str(scale))

        self.interactions.click(".size .sizes .button-size", text = str(size))
        self.interactions.click(".content-mobile .size .button.button-apply")
        if wait_closed: self.waits.not_visible(".content-mobile .size .modal")

    def select_part(self, part):
        self.interactions.click(".content .pickers .button-part[data-part='%s']" % part)

    def select_part_mobile(self, part):
        self.interactions.click(".content-mobile .pickers .button-part[data-part='%s']" % part)

    def select_material(self, material):
        self.interactions.click(".content .pickers .button-material[data-material='%s']" % material)

    def select_material_mobile(self, material):
        self.interactions.click(".content-mobile .pickers .button-material[data-material='%s']" % material)

    def select_color(self, material, color):
        self.interactions.click(".content .pickers .button-color-option[data-material='%s'][data-color='%s']" % (material, color))

    def select_color_mobile(self, material, color):
        self.interactions.click(".content-mobile .pickers .button-color-option[data-material='%s'][data-color='%s']" % (material, color))

    def assert_no_part(self, part, timeout = None):
        self.waits.not_visible(
            ".content .pickers .button-part > p",
            text = self._capitalize_words(part),
            message = "The selector for the part '%s' didn't disappear" % part,
            timeout = timeout
        )

    def assert_no_part_mobile(self, part, timeout = None):
        self.waits.not_visible(
            ".content-mobile .pickers .button-part > p",
            text = self._capitalize_words(part),
            message = "The selector for the part '%s' didn't disappear" % part,
            timeout = timeout
        )

    def assert_no_material(self, part, material):
        self.select_part(part)
        self.waits.not_visible(".material li[data-material='%s']" % material)
        self.waits.not_visible(".content .pickers .button-color[data-material='%s']" % material)

    def assert_no_material_mobile(self, part, material):
        self.select_part_mobile(part)
        self.waits.not_visible(".material li[data-material='%s']" % material)
        self.waits.not_visible(".content-mobile .pickers .button-color[data-material='%s']" % material)

    def assert_no_color(self, part, color):
        self.select_part(part)
        self.waits.not_visible(".content .pickers .button-color[data-color='%s']" % color)

    def assert_no_color_mobile(self, part, color):
        self.select_part_mobile(part)
        self.waits.not_visible(".content-mobile .pickers .button-color[data-color='%s']" % color)

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
        self.select_material(material)
        self.select_color(material, color)

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
                has_swatch = has_swatch,
                select_part = False
            )

    def set_part_mobile(
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

        This method is aimed at the mobile version of the parts selector.

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

        self.select_part_mobile(part)
        self.select_material_mobile(material)
        self.select_color_mobile(material, color)

        if verify:
            self.assert_part_mobile(
                brand,
                model,
                part,
                material,
                color,
                part_text = part_text,
                material_text = material_text,
                color_text = color_text,
                has_swatch = has_swatch,
                select_part = False
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
        has_swatch = True,
        select_part = True
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
        :type select_part: Boolean
        :param select_part: If it's true then the part that is being asserted
        is clicked before the assertions start. This is mandatory when the part
        is not selected, but unnecessary otherwise. Using this option may imply
        performance degradation as the part selection incurs animation.
        """

        if select_part: self.select_part(part)

        if part_text: self.waits.visible(".button-part.active", text = part_text)
        if color_text: self.waits.visible(".button-color-option.active", text = color_text)
        if material_text: self.waits.visible(".button-material.active", text = material_text)

        if has_swatch:
            self.waits.until(
                lambda d: self.core.assert_swatch(
                    ".content .pickers .button-part.active .swatch > img",
                    brand, model, material, color
                ),
                "Part swatch didn't have the expected image"
            )

            self.waits.until(
                lambda d: self.core.assert_swatch(
                    ".content .pickers .button-color-option.active .swatch > img",
                    brand, model, material, color
                ),
                "Color swatch didn't have the expected image"
            )

    def assert_part_mobile(
        self,
        brand,
        model,
        part,
        material,
        color,
        part_text = None,
        material_text = None,
        color_text = None,
        has_swatch = True,
        select_part = True
    ):
        """
        Checks that the part pickers have the expected state, meaning that the
        complete set of assertions are properly filled.

        If the text parameters are passed an extra set of assertions are going
        to be performed to validate expected behaviour.

        Notice that this assertion requires the changing of the current visual
        state, in the sense that the part tab is going to be switched to the
        one that is going to be asserted.

        This method is aimed at the mobile version of the parts selector.

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
        :type select_part: Boolean
        :param select_part: If it's true then the part that is being asserted
        is clicked before the assertions start. This is mandatory when the part
        is not selected, but unnecessary otherwise. Using this option may imply
        performance degradation as the part selection incurs animation.
        """

        if select_part: self.select_part_mobile(part)

        if part_text: self.waits.visible(".content-mobile .button-part.active", text = part_text)
        if color_text: self.waits.visible(" .content-mobile .button-color-option.active", text = color_text)
        if material_text: self.waits.visible(".content-mobile .button-material.active", text = material_text)

        if has_swatch:
            self.waits.until(
                lambda d: self.core.assert_swatch(
                    ".content-mobile .pickers .button-part.active .swatch > img",
                    brand, model, material, color
                ),
                "Part swatch didn't have the expected image"
            )

            self.waits.until(
                lambda d: self.core.assert_swatch(
                    ".content-mobile .pickers .button-color-option.active .swatch > img",
                    brand, model, material, color
                ),
                "Color swatch didn't have the expected image"
            )

    def url_model(self, model, brand):
        return "%s/?model=%s&brand=%s" % (self.white_url, model, brand)

    def url_product_id(self, product_id):
        return "%s/?product_id=%s" % (self.white_url, product_id)

    @property
    def base_url(self):
        return self.white_url

    @property
    def home_url(self):
        return "%s/" % self.white_url

    @property
    def next_url(self):
        return self.home_url

    @property
    def white_url(self):
        ripe_suffix = appier.conf("RIPE_SUFFIX", None)
        if ripe_suffix: white_url = "https://ripe-white-%s.platforme.com" % ripe_suffix
        else: white_url = "http://localhost:3000"
        white_url = appier.conf("BASE_URL", white_url)
        white_url = appier.conf("WHITE_URL", white_url)
        white_url = appier.conf("RIPE_WHITE_URL", white_url)
        return white_url

    def _capitalize_words(self, sentence):
        return " ".join(map(lambda s: s.capitalize(), sentence.split(" ")))
