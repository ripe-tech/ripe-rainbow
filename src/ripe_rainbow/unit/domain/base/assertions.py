#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import ripe_rainbow

class LogicPartTest(unittest.TestCase):

    def test_match_url(self):
        test_case = ripe_rainbow.TestCase()
        logic_part = ripe_rainbow.LogicPart(test_case)

        self.assertEqual(logic_part.match_url("http://www.platforme.com", "http://www.platforme.com"), True)
        self.assertEqual(logic_part.match_url("http://www.platforme.com", "http://www.platforme.come"), False)
        self.assertEqual(logic_part.match_url("http://www.platforme.com", "http://www.platforme.co"), False)

        self.assertEqual(logic_part.match_url("http://www.platforme.com", "http://www.platforme.com?param1=value1"), True)
        self.assertEqual(logic_part.match_url("http://www.platforme.com?param1=value1", "http://www.platforme.com"), True)

        self.assertEqual(logic_part.match_url(
            "http://www.platforme.com?param1=value1",
            "http://www.platforme.com",
            params = dict(param1 = "value1")
        ), True)
        self.assertEqual(logic_part.match_url(
            "http://www.platforme.com?param1=value1&param2=value2",
            "http://www.platforme.com",
            params = dict(param1 = "value1")
        ), True)
        self.assertEqual(logic_part.match_url(
            "http://www.platforme.com?param1=value1&param2=value2",
            "http://www.platforme.com",
            params = dict(param1 = "value1"),
            strict = True
        ), False)
        self.assertEqual(logic_part.match_url(
            "http://www.platforme.com?param1=value1&param2=value2",
            "http://www.platforme.com",
            params = dict(param1 = "value1", param2 = "value2"),
            strict = True
        ), True)

        self.assertEqual(logic_part.match_url(
            "http://www.platforme.com?param1=value1&param2=value2#anchor1",
            "http://www.platforme.com",
            params = dict(param1 = "value1", param2 = "value2"),
            fragment = "anchor1",
            strict = True
        ), True)
