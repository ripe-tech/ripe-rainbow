#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

class RipeIdPart(parts.Part):

    def login(self, username = None, password = None, redirect_url = None):
        username = appier.conf("RIPE_ID_USERNAME", username)
        password = appier.conf("RIPE_ID_PASSWORD", password)
        if not username or not password:
            self.owner.skip(message = "No RIPE ID credentials available")

        self.driver.get(self.base_url)

        self.interactions.click_when_possible(".button-platforme")

        self.waits.redirected_to((self.login_url, redirect_url))
        if self.driver.current_url.startswith(redirect_url): return

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        self.waits.redirected_to((self.oauth_authorize_url, redirect_url))
        if self.driver.current_url.startswith(redirect_url): return

        self.interactions.click_when_possible(".form .button-blue")

    def login_and_redirect(self, username = None, password = None, redirect_url = None):
        redirect_url = redirect_url or self.home_url
        self.login(username = username, password = password, redirect_url = redirect_url)
        self.waits.redirected_to(redirect_url)

    @property
    def id_url(self):
        id_url = appier.conf("ID_URL", "https://id.platforme.com")
        id_url = appier.conf("RIPE_ID_URL", id_url)
        return id_url

    @property
    def login_url(self):
        return "%s/admin/signin" % self.id_url

    @property
    def oauth_authorize_url(self):
        return "%s/admin/oauth/authorize" % self.id_url
