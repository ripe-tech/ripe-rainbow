# RIPE Rainbow

**Bringing happiness to the RIPE world through testing 🌈**

RIPE Rainbow is a simple automation test framework for the RIPE world.

## Installation

```bash
pip install ripe-rainbow
```

## Execution

```bash
rainbow
```

## Configuration

| Name | Type | Description |
| ----- | ----- | ----- |
| **LEVEL** | `str` | Controls the verbosity level of the attached logger (defaults to `INFO`). |
| **FILTER** | `str` | The filter regex to be used by some of the loaders (defaults to `None`). |
| **DRIVER** | `str` | The driver to be used for the interactive mode (defaults to `selenium`). |
| **TIMEOUT** | `int` | The timeout in seconds to be used by default for interactions under the interactive testing mode (defaults to `60`). |
| **SEL_MAXIMIZED** | `bool` | If the [Selenium](https://www.seleniumhq.org) driver should be started in "maximized" (window) mode (defaults to `False`). |
| **SEL_HEADLESS** | `bool` | If the [Selenium](https://www.seleniumhq.org) driver should be started in "headless" (window) mode (defaults to `False`). |

## License

RIPE Rainbow is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/ripe-tech/ripe-rainbow.svg?branch=master)](https://travis-ci.org/ripe-tech/ripe-rainbow)
[![Coverage Status](https://coveralls.io/repos/ripe-tech/ripe-rainbow/badge.svg?branch=master)](https://coveralls.io/r/ripe-tech/ripe-rainbow?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/ripe-rainbow.svg)](https://pypi.python.org/pypi/ripe-rainbow)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
