#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow

class GoogleTest(ripe_rainbow.InteractiveTestCase):

    def __init__(self, *args, **kwargs):
        ripe_rainbow.InteractiveTestCase.__init__(self, *args, **kwargs)
        ripe_rainbow.DomainWrapper.wrap_base(self)

    @property
    def google_url(self):
        return "http://www.google.com"
