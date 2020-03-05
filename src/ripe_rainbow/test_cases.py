#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import appier

import logging

from . import util
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
        self.browser_logger = kwargs.get(
            "browser_logger",
            self.__class__._build_logger(
                name = "ripe-rainbow-browser"
            )
        )

    @classmethod
    def _build_logger(
        cls,
        name = "ripe-rainbow",
        level = "INFO",
        silent = False,
        default = False
    ):
        # builds the unique instance base level name for the logger
        # and then verifies it is already registered in the class, if
        # that's the case returns the logger instance immediately
        name_i = "_logger_" + name
        memory_i = "_memory_" + name
        if hasattr(TestCase, name_i): return getattr(TestCase, name_i)

        # "computes" the proper verbosity level to be applied to the
        # standard output stream logger handler
        level = appier.conf("LEVEL", level)
        level = appier.conf("RAINBOW_LEVEL", level)
        level = logging.getLevelName(level.upper())

        # "calculates" the final value for the silent mode (no standard
        # stream handlers) taking the configuration values into consideration
        silent = appier.conf("SILENT", silent, cast = bool)
        silent = appier.conf("RAINBOW_SILENT", silent, cast = bool)

        formatter = logging.Formatter("%%(asctime)s [%s] [%%(levelname)s] %%(message)s" % name)

        logger = logging.getLogger(name)
        logger.parent = None
        logger.setLevel(logging.DEBUG)

        if not silent:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            handler.setFormatter(formatter)
            handler._name = name
            logger.addHandler(handler)

        memory_handler = appier.MemoryHandler()
        memory_handler.setLevel(logging.DEBUG)
        memory_handler.setFormatter(formatter)
        memory_handler._name = name
        logger.addHandler(memory_handler)

        setattr(TestCase, name_i, logger)
        setattr(TestCase, memory_i, memory_handler)

        memory_handlers = getattr(TestCase, "_memory_handlers", [])
        memory_handlers.append(memory_handler)
        setattr(TestCase, "_memory_handlers", memory_handlers)

        return logger

    def before(self):
        pass

    def after(self):
        memory_handlers = getattr(TestCase, "_memory_handlers", [])
        for memory_handler in memory_handlers:
            memory_handler.clear()

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
