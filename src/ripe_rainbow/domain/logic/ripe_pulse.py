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

    def click_order(self, number):
        self.interactions.click_when_possible(".table .id a[href^='/orders/%d']" % number)
        self.waits.redirected_to(self.order_url(number))
        self.waits.text(".title", "Order #%d" % number)

    def order_url(self, number):
        url = "%s/orders/%d" % (self.pulse_url, number)
        return url

    @property
    def pulse_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-pulse-ci.platforme.com")
        base_url = appier.conf("PULSE_URL", base_url)
        base_url = appier.conf("RIPE_PULSE_URL", base_url)
        return base_url

    @property
    def base_url(self):
        return self.pulse_url

    @property
    def home_url(self):
        return "%s/" % self.pulse_url

    @property
    def next_url(self):
        return self.orders_url

    @property
    def orders_url(self):
        return "%s/orders" % self.pulse_url

    @property
    def signout_url(self):
        return "%s/signout" % self.pulse_url
