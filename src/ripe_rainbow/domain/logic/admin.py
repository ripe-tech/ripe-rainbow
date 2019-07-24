#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from .. import parts

class AdminPart(parts.Part):

    def login(self, username, password):
        self.driver.get(self.signin_url)

        form = self.driver.find_element(".form")
        username_input = form.find_element_by_name("username")
        self.driver.write_text(username_input, username)
        password_input = form.find_element_by_name("password")
        self.driver.write_text(password_input, password)
        self.driver.press_enter(password_input)

    def login_wait(self, username, password):
        self.login(username, password)
        self.waits.redirected_to(self.admin_url)

    def click_forgot(self):
        self.driver.get(self.signin_url)

        forgot = self.driver.find_element(".forgot a")
        self.driver.click(forgot)

    def forgot(self, email):
        self.driver.get(self.recover_url)

        email_input = self.driver.find_element_by_name("identifier")
        self.driver.write_text(email_input, email)

        recover_button = self.driver.find_element(".base")
        self.driver.click(recover_button)

    @property
    def root_url(self):
        base_url = appier.conf("BASE_URL", "https://ripe-retail-ci.platforme.com")
        return appier.conf("ADMIN_URL", base_url)

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
