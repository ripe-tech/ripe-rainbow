#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import ripe_rainbow

def main():
    result = ripe_rainbow.ConsoleRunner().run()
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()
else:
    __path__ = []
