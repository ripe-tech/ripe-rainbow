#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeCommonsPart(parts.Part):

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
            part_text,
            material_text = None,
            color_text = None,
            verify = True,
            click_part = True,
            click_material = False,
            click_color = True,
            container_selector = ""
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
        :type click_part: bool
        :param click_part: Whether the part should be clicked or not.
        :type click_material: bool
        :param click_material: Whether the material should be clicked or not.
        :type click_color: bool
        :param click_color: Whether the color should be clicked or not.
        :type container_selector: str
        :param container_selector: The selector to restrain the picker being
        manipulated.
        """

        if click_part: self.interactions.click_when_possible(
            "%s .pickers .button-part > p:not(.no-part)" % container_selector,
            condition = lambda e: e.text == part_text
        )

        if click_material: self.interactions.click_when_possible(
            "%s .pickers .button-material[data-material='%s']" % (container_selector, material)
        )

        if click_color: self.interactions.click_when_possible(
            "%s .pickers .button-color[data-material='%s'][data-color='%s']" % (container_selector, material, color)
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
                container_selector = container_selector
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
            container_selector = ""
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
        :type container_selector: str
        :param container_selector: The selector to restrain the picker being
        asserted.
        """

        self.interactions.click_when_possible(
            "%s .pickers .button-part" % container_selector,
            condition = lambda e: e.text == part_text if part_text else part.upper()
        )

        if part_text: self.waits.text("%s .button-part.active" % container_selector, part_text)
        if color_text: self.waits.text("%s .button-color.active" % container_selector, color_text)
        if material_text: self.waits.text("%s .button-material.active" % container_selector, material_text)

        self.waits.until(
            lambda d: self.core.assert_swatch(
                "%s .pickers .button-part.active .swatch > img" % container_selector,
                brand, model, material, color
            ),
            "Part swatch didn't have the expected image."
        )
        self.waits.until(
            lambda d: self.core.assert_swatch(
                "%s .pickers .button-color.active .swatch > img" % container_selector,
                brand, model, material, color
            ),
            "Color swatch didn't have the expected image."
        )
