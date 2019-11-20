#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow

import google_base

class GoogleSearchTest(google_base.GoogleTest):

    @ripe_rainbow.test()
    def change_tracking_number(self):
        self.interactions.goto_url(self.google_url, wait = False)

        self.interactions.write_text("div.a4bIc > input", "Platforme")
        self.interactions.press_enter("div.a4bIc > input")

        self.waits.visible("div.r > a:nth-child(1) > h3 > span", text = "Platforme")
