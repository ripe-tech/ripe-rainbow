#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow

import base

class AccountLoginTest(base.RetailTest):

    @ripe_rainbow.test
    def valid_login(self):
        self.retail.login_and_redirect("fendi.test", "password")

    @ripe_rainbow.test
    def invalid_username_login(self):
        self.retail.login("invalidUsername", "root")

        self.waits.text(
            ".error",
            "No valid account found"
        )

    @ripe_rainbow.test
    def invalid_password_login(self):
        self.retail.login("fendi.test", "invalidPassword")

        self.waits.text(
            ".error",
            "Invalid or mismatch password"
        )

    @ripe_rainbow.test
    def invalid_empty_login(self):
        self.retail.login("", "")

        self.waits.text(
            ".error",
            ""
        )
