#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

class RipeIdPart(parts.Part):

    def login(self, username, password):
        self.driver.get(self.base_url)
        self.interactions.click_when_possible(".button-platforme")

        self.waits.redirected_to(self.id_url)

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def login_and_redirect(self, username, password):
        self.login(username, password)
        self.waits.redirected_to(self.base_url)

    @property
    def id_url(self):
        return appier.conf("ID_URL", "https://id.platforme.com")
