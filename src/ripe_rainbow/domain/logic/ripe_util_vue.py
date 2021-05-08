#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeUtilVuePart(parts.Part):

    def login_wait(self, environment = "ci", redirect_url = None):
        self._login_wait(redirect_url)
        self.waits.visible(".top-bar .center .selector .title")
        self.interactions.goto_url(
            redirect_url or self.home_url,
            params = [
                ("env", [environment])
            ]
        )
        self.waits.visible(".top-bar .center .selector .selection", text = environment)

    def logout_wait(self):
        self.interactions.goto_url(self.signout_url, redirect_url = (self.home_url, self.id.login_url))

    def _login_wait(self, redirect_url = None):
        self.interactions.goto_url(self.home_url, redirect_url = (self.home_url, self.id.login_url))
        self.id.authorize(redirect_url = self.next_url)

        redirect_url = redirect_url or self.home_url
        if self.interactions.url.startswith(redirect_url): return

        self.interactions.click(".form .button-blue")
        self.waits.redirected_to(redirect_url)

    @property
    def util_vue_url(self):
        util_vue_url = "https://ripe-util-vue.platforme.com"
        util_vue_url = appier.conf("BASE_URL", util_vue_url)
        util_vue_url = appier.conf("UTIL_VUE_URL", util_vue_url)
        util_vue_url = appier.conf("RIPE_UTIL_VUE_URL", util_vue_url)
        return util_vue_url

    @property
    def base_url(self):
        return self.util_vue_url

    @property
    def home_url(self):
        return "%s/" % self.util_vue_url

    @property
    def next_url(self):
        return self.home_url

    @property
    def signout_url(self):
        return "%s/signout" % self.util_vue_url

    @property
    def delivery_url(self):
        return "%s/delivery" % self.base_url

    @property
    def example_url(self):
        return "%s/example" % self.base_url

    @property
    def locales_url(self):
        return "%s/locales" % self.base_url

    @property
    def order_url(self):
        return "%s/order" % self.base_url

    @property
    def orders_url(self):
        return "%s/orders" % self.base_url

    @property
    def platforme_id_url(self):
        return "%s/platforme-id" % self.base_url

    @property
    def quote_url(self):
        return "%s/quote" % self.base_url

    @property
    def rules_url(self):
        return "%s/rules" % self.base_url

    @property
    def background_url(self):
        return "%s/background" % self.base_url
