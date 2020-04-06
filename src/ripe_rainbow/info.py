#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

NAME = "RIPE Rainbow"
VERSION = "0.7.7"
RAINBOW = "🌈"
LABEL = "%s %s %s" % (NAME, VERSION, RAINBOW)
PLATFORM = "%s %d.%d.%d.%s %s" % (
    sys.subversion[0] if hasattr(sys, "subversion") else "CPython",
    sys.version_info[0],
    sys.version_info[1],
    sys.version_info[2],
    sys.version_info[3],
    sys.platform
)
LABEL_FULL = "%s (%s)" % (LABEL, PLATFORM)
