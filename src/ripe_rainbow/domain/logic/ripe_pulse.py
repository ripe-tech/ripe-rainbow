#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipePulsePart(parts.Part):

    def login(self):
        self.id.login()

    def login_wait(self, redirect_url = None):
        self.id.login_wait(redirect_url = redirect_url)

    def logout(self):
        self.driver.get(self.signout_url)

    def logout_wait(self, redirect_url = None):
        redirect_url = redirect_url or self.home_url
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
        return "%s/" % self.base_url

    @property
    def next_url(self):
        return self.orders_url

    @property
    def orders_url(self):
        return "%s/orders" % self.base_url

    @property
    def signout_url(self):
        return "%s/signout" % self.base_url
