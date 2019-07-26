#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeCorePart(parts.Part):

    def assert_swatch(self, selector, brand, model, material, color):
        """
        Checks that the img element identified by the selector points to the
        correct swatch. The correctness verification is performed by checking
        the `src` attribute of the element.

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
        :rtype: bool
        :return: If the assertion was successful or not (propagation).
        """

        element = self.waits.element(selector)
        return self.assertions.match_url(
            element.get_attribute("src"),
            self.swatch_url,
            params = dict(
                brand = brand,
                model = model,
                material = material,
                color = color
            )
        )

    def wait_initials_image(self, selector, model, initials):
        return self.waits.until(
            lambda d: self.assert_initials_image(selector, model, initials),
            "Personalization image was not the expected one."
        )

    def assert_initials_image(self, selector, model, initials):
        expected_params = dict(
            initials = initials,
            model = model
        )

        element = self.waits.element(selector)
        src = element.get_attribute("src")

        return self.assertions.match_url(src, self.compose_url, params = expected_params)

    def order_url(self, number):
        return "%s/orders/%d" % (self.api_url, number)

    def report_pdf_url(self, number, key = None):
        url = "%s/orders/%d/report.pdf" % (self.api_url, number)
        if key: url += "?key=%s" % appier.util.quote(key)
        return url

    @property
    def core_url(self):
        core_url = appier.conf("CORE_URL", "https://ripe-core-ci.platforme.com")
        core_url = appier.conf("RIPE_CORE_URL", core_url)
        return core_url

    @property
    def base_url(self):
        return self.core_url

    @property
    def api_url(self):
        return "%s/api" % self.core_url

    @property
    def orders_url(self):
        return "%s/orders" % self.api_url

    @property
    def swatch_url(self):
        return "%s/swatch" % self.api_url

    @property
    def compose_url(self):
        return "%s/compose" % self.api_url
