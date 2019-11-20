#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow

import google_base

class GoogleSearchTest(google_base.GoogleTest):

    @ripe_rainbow.test()
    def search_platforme(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Platforme")
        self.interactions.press_enter("div.a4bIc > input")

        self.waits.visible("div.g:nth-child(1) h3 > span", text = "Platforme")

    @ripe_rainbow.test()
    def search_google(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Google")
        self.interactions.press_enter("div.a4bIc > input")

        self.waits.visible("div.g:nth-child(1) h3 > span", text = "Google")
