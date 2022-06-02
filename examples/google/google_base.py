#!/usr/bin/python
# -*- coding: utf-8 -*-

import ripe_rainbow


class GoogleTest(ripe_rainbow.InteractiveTestCase):
    def __init__(self, *args, **kwargs):
        ripe_rainbow.InteractiveTestCase.__init__(self, *args, **kwargs)
        ripe_rainbow.DomainWrapper.wrap_base(self)

    @property
    def driver_args(self):
        args = dict()
        if self.is_mobile:
            args.update(mobile=True, device="nexus5", resolution="360x640", pixel_ratio=3)
        if self.is_tablet:
            args.update(
                mobile=True, device="galaxytab3", resolution="768x1024", pixel_ratio=3
            )
        return args

    @property
    def is_mobile(self):
        return False

    @property
    def is_tablet(self):
        return False

    @property
    def google_url(self):
        return "http://www.google.com"
