#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

class Loader(object):

    def test_suite(self):
        raise appier.NotImplementedError()

class PathLoader(Loader):

    def __init__(self, path = "."):
        self.path = path

    def test_suite(self):
        # @todo tenho de procurar os ficheiros no path
        # e tentar correr os mesmos, depois de os improtar
        pass
