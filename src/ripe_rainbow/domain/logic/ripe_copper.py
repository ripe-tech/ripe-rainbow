#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeCopperPart(parts.Part):

    def logout(self):
        self.driver.get(self.signout_url)

    def logout_and_redirect(self, redirect_url = None):
        redirect_url = redirect_url or self.home_url
        self.logout()
        if first:
            self.waits.redirected_to(redirect_url)
            first = True
        else:
            self.waits.redirected_to(redirect_url)

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-copper-ci.platforme.com")
        base_url = appier.conf("COPPER_URL", base_url)
        base_url = appier.conf("RIPE_COPPER_URL", base_url)
        return base_url

    @property
    def home_url(self):
        return "%s/search" % self.base_url

    @property
    def signout_url(self):
        return "%s/signout" % self.base_url
