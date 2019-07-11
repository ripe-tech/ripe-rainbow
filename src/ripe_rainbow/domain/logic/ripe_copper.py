#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeCopperPart(parts.Part):

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-copper-ci.platforme.com")
        base_url = appier.conf("COPPER_URL", base_url)
        base_url = appier.conf("RIPE_COPPER_URL", base_url)
        return base_url

    @property
    def home_url(self):
        return "%s/search" % self.base_url
