#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import ripe_rainbow

from . import mock

class UtilTest(unittest.TestCase):

    def test_test_fullname(self):
        test_case = mock.DemoTestCase()
        result = ripe_rainbow.test_fullname(test_case.test_empty)

        self.assertEqual(result, "ripe_rainbow.unit.mock.DemoTestCase.test_empty")
