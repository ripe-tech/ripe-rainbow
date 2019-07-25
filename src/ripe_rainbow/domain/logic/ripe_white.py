#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeWhitePart(parts.Part):

    def select_size(self, size, gender = None, scale = None, open = True):
        return self.commons.select_size(
            size,
            gender = gender,
            scale = scale,
            open = open
        )

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
            click_material = True,
            container_selector = ".content"
    ):
        return self.commons.set_part(
            brand,
            model,
            part,
            material,
            color,
            part_text = part_text if part_text else part.capitalize(),
            material_text = material_text,
            color_text = color_text,
            verify = verify,
            click_material = click_material,
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
            color_text = None
    ):
        return self.commons.assert_part(
            brand,
            model,
            part,
            material,
            color,
            part_text = part_text,
            material_text = material_text,
            color_text = color_text
        )

    def url_model(self, model, brand):
        return "%s/?model=%s&brand=%s" % (self.white_url, model, brand)

    def url_product_id(self, product_id):
        return "%s/?product_id=%s" % (self.white_url, product_id)

    @property
    def base_url(self):
        return self.white_url

    @property
    def white_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-white-ci.platforme.com")
        base_url = appier.conf("WHITE_URL", base_url)
        base_url = appier.conf("RIPE_WHITE_URL", base_url)
        return base_url
