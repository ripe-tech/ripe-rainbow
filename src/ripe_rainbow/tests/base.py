#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow

class RetailTest(ripe_rainbow.InteractiveTestCase):

    def __init__(self, *args, **kwargs):
        ripe_rainbow.InteractiveTestCase.__init__(self, *args, **kwargs)
        ripe_rainbow.DomainWrapper.wrap_base(self)
        ripe_rainbow.DomainWrapper.wrap_retail(self)
