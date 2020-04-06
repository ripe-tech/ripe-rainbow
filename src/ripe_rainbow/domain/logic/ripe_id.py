#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class RipeIdPart(parts.Part):

    def login(self, username = None, password = None, redirect_url = None):
        self.interactions.goto_url(self.home_url)

        self.interactions.click(".button-platforme")
        self.authorize(redirect_url = redirect_url)

        if self.interactions.url.startswith(redirect_url): return

        self.interactions.click(".form .button-blue")

    def login_wait(self, username = None, password = None, redirect_url = None):
        redirect_url = redirect_url or self.next_url
        self.login(
            username = username,
            password = password,
            redirect_url = redirect_url
        )
        self.waits.redirected_to(redirect_url)

    def logout(self):
        self.interactions.goto_url(self.logout_url)

    def logout_wait(self, redirect_url = None):
        redirect_url = redirect_url or self.login_url
        self.logout()
        self.waits.redirected_to(redirect_url)

    def authorize(self, username = None, password = None, redirect_url = None):
        redirect_url = redirect_url or self.next_url
        username = appier.conf("RIPE_ID_USERNAME", username)
        password = appier.conf("RIPE_ID_PASSWORD", password)
        if not username or not password:
            self.skip(message = "No RIPE ID credentials available")

        self.waits.redirected_to((self.login_url, redirect_url))
        if self.interactions.url.startswith(redirect_url): return

        self.interactions.write_text(".form input[name='username']", username)
        self.interactions.write_text(".form input[name='password']", password)
        self.interactions.press_enter(".form input[name='password']")

        self.waits.redirected_to((self.oauth_authorize_url, redirect_url))

    @property
    def id_url(self):
        id_url = appier.conf("ID_URL", "https://id.platforme.com")
        id_url = appier.conf("RIPE_ID_URL", id_url)
        return id_url

    @property
    def base_url(self):
        return self.id_url

    @property
    def login_url(self):
        return "%s/admin/signin" % self.id_url

    @property
    def logout_url(self):
        return "%s/admin/signout" % self.id_url

    @property
    def oauth_authorize_url(self):
        return "%s/admin/oauth/authorize" % self.id_url
