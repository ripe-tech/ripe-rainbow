#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import ripe_rainbow

class EventsTest(unittest.TestCase):

    def test_event_stringifier(self):
        event = "Network.requestWillBeSent"
        stringifier = ripe_rainbow.interactive.events.EVENT_STRINGIFIERS[event]
        self.assertEqual(stringifier, ripe_rainbow.interactive.events.stringify_request_will_be_sent)

        event = "Network.responseReceived"
        stringifier = ripe_rainbow.interactive.events.EVENT_STRINGIFIERS[event]
        self.assertEqual(stringifier, ripe_rainbow.interactive.events.stringify_response_received)

    def test_stringify_response_received(self):
        message_j = dict(
            method = "Network.responseReceived",
            params = dict(
                requestId = "3D8A8C5C9832597801E08A06FA29E4C0",
                timestmap = 1987.4121,
                response = dict(
                    connectionId = 11,
                    headers = {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "text/html"
                    },
                    status = 200,
                    url = "https://platforme.com",
                )
            )
        )
        log = ripe_rainbow.interactive.events.stringify_response_received(message_j)
        expected = "Network.responseReceived 3D8A8C5C9832597801E08A06FA29E4C0 200 https://platforme.com {'Access-Control-Allow-Origin': '*', 'Content-Type': 'text/html'}"
        self.assertEqual(log, expected)

    def test_stringify_request_will_be_sent(self):
        message_j = dict(
            method = "Network.requestWillBeSent",
            params = dict(
                requestId = "3D8A8C5C9832597801E0",
                timestamp = 1987.03854,
                request = dict(
                    method = "GET",
                    url = "https://platforme.com",
                    headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                    }
                )
            )
        )
        log = ripe_rainbow.interactive.events.stringify_request_will_be_sent(message_j)
        expected = "Network.requestWillBeSent 3D8A8C5C9832597801E0 GET https://platforme.com {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}"
        self.assertEqual(log, expected)
