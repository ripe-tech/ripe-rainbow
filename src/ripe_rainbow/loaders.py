#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import inspect

import appier

from . import test_cases

class Loader(object):

    def test_suite(self, **kwargs):
        raise appier.NotImplementedError()

class PathLoader(Loader):

    def __init__(self, path = None):
        self.path = path or "."
        self.path = os.path.expanduser(self.path)
        self.path = os.path.abspath(self.path)
        self.path = os.path.normpath(self.path)

    def test_suite(self, **kwargs):
        return [test_cls(loader = self, **kwargs) for test_cls in self._load_classes(self.path)]

    def _load_classes(self, path, recursive = True):
        classes = []
        modules = self._load_modules(path, recursive = recursive)

        # iterates over the complete set of loaded modules to try
        # to load all of the test classes contained in them
        for module in modules:

            # uses the path to the module containing the test to try
            # to gather some context to the test, this means that the
            # name of the directory is going to be used as some kind
            # of context for the test execution
            module_path = module.__file__ if hasattr(module, "__file__") else None
            module_path = module_path or None
            if module_path:
                module_path = os.path.normpath(os.path.abspath(module_path))
                ctx = os.path.basename(os.path.dirname(module_path))
            else:
                ctx = None

            for name in dir(module):
                value = getattr(module, name)
                if not inspect.isclass(value): continue
                if not issubclass(value, test_cases.TestCase): continue
                value.ctx = ctx
                classes.append(value)

        return classes

    def _load_packages(self, path, recursive = True):
        packages = []

        if os.path.isdir(path):
            name = os.path.basename(path)
            dir_path = os.path.dirname(path)
            base_name = os.path.splitext(name)[0]
            sys.path.insert(0, dir_path)
            try:
                packages.append(__import__(base_name))
            except ImportError:
                pass
            finally:
                sys.path.remove(dir_path)

        names = os.listdir(path)
        for name in names:
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path) and recursive:
                packages += self._load_packages(full_path, recursive = recursive)

        return packages

    def _load_modules(self, path, recursive = True):
        modules = []
        names = os.listdir(path)
        if not "." in sys.path: sys.path.insert(0, ".")
        for name in names:
            base_name = os.path.splitext(name)[0]
            full_path = os.path.join(path, name)
            if os.path.isdir(full_path) and recursive:
                modules += self._load_modules(full_path, recursive = recursive)
            elif name.endswith(".py"):
                sys.path.insert(0, path)
                try:
                    modules.append(__import__(base_name))
                except (ImportError, ValueError):
                    pass
                finally:
                    sys.path.remove(path)
        return modules
