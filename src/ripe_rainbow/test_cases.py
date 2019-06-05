#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

class TestCase(object):

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.runner = kwargs.get("runner", None)
        self.loader = kwargs.get("loader", None)
        self.logger = kwargs.get("logger", logging.getLogger("test"))

    def before(self):
        pass

    def after(self):
        pass

    def run_all(self):
        for test in self.tests():
            self.run_test(test)

    def run_test(self, test):
        self.before()
        try:
            test()
        finally:
            self.after()

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

    @property
    def tests(self):
        return [getattr(self, name) for name in dir(self) if not name == "tests" and hasattr(getattr(self, name), "test")]
