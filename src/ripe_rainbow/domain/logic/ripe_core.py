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

        element = self.waits.visible(selector, ensure = False)
        return self.logic.match_url(
            element.get_attribute("src"),
            self.swatch_url,
            params = dict(
                brand = brand,
                model = model,
                material = material,
                color = color
            )
        )

    def wait_initials_image(self, selector, model, initials, profile = None):
        return self.waits.until(
            lambda d: self.assert_initials_image(
                selector,
                model,
                initials,
                profile = profile
            ),
            "Personalization image was not the expected one"
        )

    def assert_initials_image(self, selector, model, initials, profile = None):
        expected_params = dict(
            initials = initials,
            model = model
        )

        if profile: expected_params["initials_profile"] = profile

        element = self.waits.visible(selector, ensure = False)
        src = element.get_attribute("src")

        return self.logic.match_url(src, self.compose_url, params = expected_params)

    def order_url(self, number):
        return "%s/orders/%d" % (self.api_url, number)

    def report_pdf_url(self, number, key = None):
        url = "%s/orders/%d/report.pdf" % (self.api_url, number)
        if key: url += "?key=%s" % appier.util.quote(key)
        return url

    @property
    def core_url(self):
        ripe_suffix = appier.conf("RIPE_SUFFIX", None)
        if ripe_suffix: core_url = "https://ripe-core-%s.platforme.com" % ripe_suffix
        else: core_url = "http://localhost:8080"
        core_url = appier.conf("CORE_URL", core_url)
        core_url = appier.conf("RIPE_CORE_URL", core_url)
        return core_url

    @property
    def username(self):
        username = appier.conf("CORE_USERNAME", "root")
        username = appier.conf("RIPE_CORE_USERNAME", username)
        return username

    @property
    def password(self):
        password = appier.conf("CORE_PASSWORD", "root")
        password = appier.conf("RIPE_CORE_PASSWORD", password)
        return password

    @property
    def base_url(self):
        return self.core_url

    @property
    def api_url(self):
        return "%s/api" % self.core_url

    @property
    def admin_url(self):
        return "%s/admin" % self.core_url

    @property
    def admin_api_url(self):
        return "%s/api/admin" % self.core_url

    @property
    def export_url(self):
        return "%s/export" % self.core_url

    @property
    def export_api_url(self):
        return "%s/api/export" % self.core_url

    @property
    def orders_url(self):
        return "%s/orders" % self.api_url

    @property
    def swatch_url(self):
        return "%s/swatch" % self.api_url

    @property
    def compose_url(self):
        return "%s/compose" % self.api_url
