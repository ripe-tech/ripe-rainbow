#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow

class DemoTestCase(ripe_rainbow.TestCase):

    @ripe_rainbow.test()
    def test_empty(self):
        pass
