#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import appier

import logging

from . import errors

class TestCase(appier.Observable):

    def __init__(self, *args, **kwargs):
        appier.Observable.__init__(self, *args, **kwargs)
        self.runner = kwargs.get("runner", None)
        self.loader = kwargs.get("loader", None)
        self.logger = kwargs.get("logger", self.__class__._build_logger(default = True))
        self.breadcrumbs = kwargs.get(
            "breadcrumbs",
            self.__class__._build_logger(
                name = "ripe-rainbow-breadcrumbs"
            )
        )

    @classmethod
    def _build_logger(cls, name = "ripe-rainbow", level = "INFO", default = False):
        name_i = "_logger_" + name
        if hasattr(TestCase, name_i): return getattr(TestCase, name_i)
        level = appier.conf("LEVEL", level)
        level = appier.conf("RAINBOW_LEVEL", level)
        level = logging.getLevelName(level.upper())
        formatter = logging.Formatter("%%(asctime)s [%s] [%%(levelname)s] %%(message)s" % name)
        logger = logging.getLogger(name)
        logger.parent = None
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.setLevel(level)
        setattr(TestCase, name_i, logger)
        return logger

    def before(self):
        pass

    def after(self):
        pass

    def succeeded(self, test, ctx = None):
        pass

    def failed(self, test, exception, ctx = None):
        pass

    def skipped(self, test):
        pass

    def run_all(self):
        for test in self.tests():
            self.run_test(test)

    def run_test(self, test, ctx = None):
        self.before()
        try:
            test()
            self.succeeded(test, ctx = ctx)
        except errors.SkipError:
            self.skipped(test)
            raise
        except Exception as exception:
            self.failed(test, exception, ctx = ctx)
            raise
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

    def pause(self, timeout = 86400):
        time.sleep(timeout)

    def skip(self, message = None, reason = None):
        raise errors.SkipError(
            message = message,
            reason = reason or message
        )

    @property
    def tests(self):
        return [
            getattr(self, name) for name in dir(self)
            if not name == "tests" and hasattr(getattr(self, name), "test")
        ]
