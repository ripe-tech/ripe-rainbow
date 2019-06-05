#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import inspect

import appier

from . import test_cases

class Loader(object):

    def test_suite(self):
        raise appier.NotImplementedError()

class PathLoader(Loader):

    def __init__(self, path = "."):
        self.path = os.path.normpath(os.path.abspath(os.path.expanduser(path)))

    def test_suite(self):
        return [test_cls() for test_cls in self._test_classes(self.path)]

    def _test_classes(self, path, recursive = True):
        classes = []
        modules = self._test_modules(path, recursive = recursive)
        for module in modules:
            for name in dir(module):
                value = getattr(module, name)
                if not inspect.isclass(value): continue
                if not issubclass(value, test_cases.TestCase): continue
                classes.append(value)
        return classes

    def _test_modules(self, path, recursive = True):
        modules = []
        names = os.listdir(path)
        for name in names:
            base_name = os.path.splitext(name)[0]
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path) and recursive:
                modules += self._test_modules(full_path, recursive = recursive)
            elif name.endswith(".py"):
                sys.path.insert(0, path)
                try:
                    modules.append(__import__(base_name))
                except ImportError:
                    pass
                finally:
                    sys.path.remove(path)
        return modules
