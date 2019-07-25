#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeWhitePart(parts.Part):

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
