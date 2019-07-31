#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import setuptools

setuptools.setup(
    name = "ripe-rainbow",
    version = "0.4.2",
    author = "Platforme International",
    author_email = "development@platforme.com",
    description = "RIPE Rainbow",
    license = "Apache License, Version 2.0",
    keywords = "ripe rainbow test",
    url = "http://www.platforme.com",
    zip_safe = False,
    packages = [
        "ripe_rainbow",
        "ripe_rainbow.domain",
        "ripe_rainbow.domain.base",
        "ripe_rainbow.domain.logic",
        "ripe_rainbow.interactive",
        "ripe_rainbow.unit",
        "ripe_rainbow.unit.domain",
        "ripe_rainbow.unit.domain.base"
    ],
    test_suite = "ripe_rainbow.unit",
    package_dir = {
        "" : os.path.normpath("src")
    },
    entry_points = {
        "console_scripts" : [
            "rainbow = ripe_rainbow.main:main",
            "ripe-rainbow = ripe_rainbow.main:main"
        ]
    },
    install_requires = [
        "appier"
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
