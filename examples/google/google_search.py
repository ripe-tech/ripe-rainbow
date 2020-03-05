#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import ripe_rainbow

import google_base

class GoogleSearchTest(google_base.GoogleTest):

    @ripe_rainbow.test()
    def search_platforme(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Platforme")
        self.interactions.press_enter("div.a4bIc > input")

        self.waits.visible("div.g:nth-child(1) h3", text = "Platforme")

    @ripe_rainbow.test()
    def search_google(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Google")
        self.interactions.press_enter("div.a4bIc > input")

        self.waits.visible("div.g:nth-child(1) h3", text = "Google")

    @ripe_rainbow.test()
    def search_highlight(self):
        self.interactions.goto_url(self.google_url, wait = False)

        element = self.waits.visible("div.a4bIc > input")
        element._highlight()

        self.interactions.write_text("div.a4bIc > input", "Highlight works !!!")

        time.sleep(2.5)

        element = self.waits.visible("div.a4bIc > input")
        element._lowlight()

        self.interactions.write_text("div.a4bIc > input", " ... Lowlight also works !!!")

        time.sleep(2.5)
