#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

class RetailPart(parts.Part):

    def login(self, username, password):
        self.driver.get(self.login_url)

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def login_and_redirect(self, username, password):
        self.login(username, password)

        self.waits.redirected_to(self.base_url)

    def select_size(self, size, scale):
        self.interactions.click_when_possible(".size:not(.disabled) .button-size")

        self.interactions.click_when_possible(
            ".size .button-scale",
            condition = lambda element: element.text == str(scale)
        )
        self.waits.element(
            ".size .button-scale.active",
            condition = lambda element: element.text == str(scale)
        )

        self.interactions.click_when_possible(
            ".size .button-size",
            condition = lambda element: element.text == str(size)
        )

        self.interactions.click_when_possible(".size .button.button-primary.button-apply")
        self.waits.is_not_visible(".size .modal-container")

    @property
    def base_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-retail-test.platforme.com")
        return appier.conf("RETAIL_URL", base_url)

    @property
    def login_url(self):
        return "%s/login" % self.base_url

    @property
    def logout_url(self):
        return "%s/logout" % self.base_url
