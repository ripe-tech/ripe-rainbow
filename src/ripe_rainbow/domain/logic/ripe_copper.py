#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeCopperPart(parts.Part):

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
    def copper_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-copper-ci.platforme.com")
        base_url = appier.conf("COPPER_URL", base_url)
        base_url = appier.conf("RIPE_COPPER_URL", base_url)
        return base_url

    @property
    def base_url(self):
        return self.copper_url

    @property
    def home_url(self):
        return "%s/" % self.copper_url

    @property
    def next_url(self):
        return self.search_url

    @property
    def search_url(self):
        return "%s/search" % self.copper_url

    @property
    def signout_url(self):
        return "%s/signout" % self.copper_url
