#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipePulsePart(parts.Part):

    def logout(self):
        self.driver.get(self.signout_url)

    def logout_and_redirect(self, redirect_url = None):
        redirect_url = redirect_url or self.base_url
        self.logout()
        self.waits.redirected_to(redirect_url)

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-pulse-ci.platforme.com")
        base_url = appier.conf("PULSE_URL", base_url)
        base_url = appier.conf("RIPE_PULSE_URL", base_url)
        return base_url

    @property
    def home_url(self):
        return "%s/orders" % self.base_url

    @property
    def signout_url(self):
        return "%s/signout" % self.base_url
