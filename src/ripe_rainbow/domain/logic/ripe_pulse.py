#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipePulsePart(parts.Part):

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-pulse-ci.platforme.com")
        base_url = appier.conf("PULSE_URL", base_url)
        base_url = appier.conf("RIPE_PULSE_URL", base_url)
        return base_url

    @property
    def home_url(self):
        return "%s/orders" % self.base_url
