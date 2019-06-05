#!/usr/bin/python
# -*- coding: utf-8 -*-

class TestCase(object):

    def error(self, message):
        if not self.logger: return
        self.logger.error(message)

    def warning(self, message):
        if not self.logger: return
        self.logger.warning(message)

    def info(self, message):
        if not self.logger: return
        self.logger.info(message)

    def debug(self, message):
        if not self.logger: return
        self.logger.debug(message)

    def log_stack(self, method = None):
        pass

class InteractiveTestCase(TestCase):

    def get_driver(self):
        pass

class InteractiveDriver(object):

    def start(self):
        pass

    def stop(self):
        pass

class SeleniumTestCase(InteractiveDriver):
    pass
