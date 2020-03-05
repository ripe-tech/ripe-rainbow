#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class AdminPart(parts.Part):

    def login(self, username, password):
        self.interactions.goto_url(self.signin_url)

        self.interactions.write_text(".form input[name='username']", username)
        self.interactions.write_text(".form input[name='password']", password)
        self.interactions.press_enter(".form input[name='password']")

    def login_wait(self, username, password):
        self.login(username, password)
        self.waits.redirected_to(self.admin_url)

    def click_forgot(self):
        self.interactions.goto_url(self.signin_url)

        self.interactions.click(".forgot a")

    def forgot(self, email):
        self.interactions.goto_url(self.recover_url)

        self.interactions.write_text("input[name='identifier']", email)
        self.interactions.click(".button")

    @property
    def root_url(self):
        ripe_suffix = appier.conf("RIPE_SUFFIX", None)
        if ripe_suffix: root_url = "https://ripe-core-%s.platforme.com" % ripe_suffix
        else: root_url = "http://localhost:8080"
        root_url = appier.conf("BASE_URL", root_url)
        root_url = appier.conf("CORE_URL", root_url)
        root_url = appier.conf("RIPE_CORE_URL", root_url)
        root_url = appier.conf("ADMIN_URL", root_url)
        return appier.conf("RIPE_ADMIN_URL", root_url)

    @property
    def username(self):
        username = appier.conf("CORE_USERNAME", "root")
        username = appier.conf("RIPE_CORE_USERNAME", username)
        username = appier.conf("ADMIN_USERNAME", username)
        username = appier.conf("RIPE_ADMIN_USERNAME", username)
        return username

    @property
    def password(self):
        password = appier.conf("CORE_PASSWORD", "root")
        password = appier.conf("RIPE_CORE_PASSWORD", password)
        password = appier.conf("ADMIN_PASSWORD", password)
        password = appier.conf("RIPE_ADMIN_PASSWORD", password)
        return password

    @property
    def admin_url(self):
        return "%s/admin" % self.root_url

    @property
    def base_url(self):
        return self.admin_url

    @property
    def signin_url(self):
        return "%s/signin" % self.admin_url

    @property
    def recover_url(self):
        return "%s/recover" % self.admin_url
