#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import ripe_rainbow

import google_base

class GoogleTabletTest(google_base.GoogleTest):

    @property
    def is_tablet(self):
        return True

    @ripe_rainbow.test()
    def search_platforme(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Platforme")
        self.interactions.press_enter("div.a4bIc > input")

        self.waits.visible("div:nth-child(1) > div > div > div > a > div > div", text = "Platforme")

    @ripe_rainbow.test()
    def search_highlight(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Platforme")
        self.interactions.press_enter("div.a4bIc > input")

        element = self.waits.visible("div:nth-child(1) > div > div > div > a > div > div", text = "Platforme")
        element._highlight()
        element._focus()

        time.sleep(2.5)
