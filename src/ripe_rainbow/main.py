#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

import ripe_rainbow

def main():
    class_filter = sys.argv[1] if len(sys.argv) > 1 else None
    class_filter = re.compile(class_filter) if class_filter else None

    result = ripe_rainbow.ConsoleRunner(class_filter = class_filter).run()
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main()
else:
    __path__ = []
