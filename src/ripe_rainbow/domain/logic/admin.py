#!/usr/bin/python
# -*- coding: utf-8 -*-

try: from selenium.webdriver.common.keys import Keys
except ImportError: Keys = None

from .. import parts

class AdminPart(parts.Part):

    def base_url(self):
        return "%s/admin" % self.inner_base_url

    def signin_url(self):
        return "%s/signin" % self.base_url()

    def recover_url(self):
        return "%s/recover" % self.base_url()

    def login(self, username, password):
        self.driver.get(self.signin_url())

        form = self.driver.find_element_by_css_selector(".form")
        username_input = form.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = form.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def login_and_redirect(self, username, password):
        self.login(username, password)

        self.waits.redirected_to(self.base_url())

    def click_forgot(self):
        self.driver.get(self.signin_url())

        forgot = self.driver.find_element_by_css_selector(".forgot a")
        forgot.click()

    def forgot(self, email):
        self.driver.get(self.recover_url())

        email_input = self.driver.find_element_by_name("identifier")
        email_input.send_keys(email)

        recover_button = self.driver.find_element_by_css_selector(".base")
        recover_button.click()

        self.waits.redirected_to(self.base_url())
