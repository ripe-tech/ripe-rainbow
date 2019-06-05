#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys

from .. import parts

class RetailPart(parts.Part):

    def __init__(self, base_url, driver, waits):
        self.inner_base_url = base_url
        self.driver = driver
        self.waits = waits

    def base_url(self):
        return "%s" % self.inner_base_url

    def login_url(self):
        return "%s/login" % self.base_url()

    def logout_url(self):
        return "%s/logout" % self.base_url()

    def login(self, username, password):
        self.driver.get(self.login_url())

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def login_and_redirect(self, username, password):
        self.login(username, password)

        self.waits.redirected_to(self.base_url())
