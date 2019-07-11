#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

class RipeIdPart(parts.Part):

    def login(self, username = None, password = None):
        username = appier.conf("RIPE_ID_USERNAME", username)
        password = appier.conf("RIPE_ID_PASSWORD", password)
        if not username or not password:
            self.owner.skip(message = "No RIPE ID credentials available")

        self.driver.get(self.base_url)

        self.interactions.click_when_possible(".button-platforme")
        self.waits.redirected_to(self.login_url)

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        self.interactions.click_when_possible(".form .button-blue")

    def login_and_redirect(self, username = None, password = None):
        self.login(username = username, password = password)
        self.waits.redirected_to(self.home_url)

    @property
    def id_url(self):
        return appier.conf("ID_URL", "https://id.platforme.com")

    @property
    def login_url(self):
        return "%s/admin/signin" % self.id_url
