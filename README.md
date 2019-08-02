# [![RIPE Rainbow](res/logo.png)](https://tech.platforme.com)

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
| **TIMEOUT** | `int` | The timeout in seconds to be used by default for interactions under the interactive testing mode (defaults to `15`). |
| **REPEAT** | `int` | The number of times to repeat the execution of the tests (defaults to `1`). |
| **STACKTRACES** | `bool` | If "stacktrace" log should be stored on failure of tests (defaults to `false`). |
| **STACKTRACES_PATH** | `bool` | The base path to be used to save the stacktraces log (defaults to `.`). |
| **SCREENSHOTS** | `bool` | If screenshots should be save on failure of tests (defaults to `false`). |
| **SCREENSHOTS_PATH** | `bool` | The base path to be used to save the screenshots (defaults to `.`). |
| **SEL_SECURE** | `bool` | If the [Selenium](https://www.seleniumhq.org) engine should be executed under a secure approach (should be slower) (defaults to `False`). |
| **SEL_BROWSER** | `str` | The browser engine that is going to be used by Selenium (eg: `chrome`, `firefox`) (defaults to `chrome`). |
| **SEL_MAXIMIZED** | `bool` | If the [Selenium](https://www.seleniumhq.org) driver should be started in "maximized" (window) mode (defaults to `False`). |
| **SEL_HEADLESS** | `bool` | If the [Selenium](https://www.seleniumhq.org) driver should be started in "headless" (window) mode (defaults to `False`). |
| **SEL_WINDOW_SIZE** | `str` | Resolution (in pixels) that the [Selenium](https://www.seleniumhq.org) driver will use for the window (defaults to `1920x1080`). |
| **SEL_SERVICE_ARGS** | `list` | List of command line args to be passed to the driver service that interacts with the browser (defaults to `[]`). |
| **SEL_POLL_FREQUENCY** | `float` | The frequency (in seconds) to run the [busy waiting](https://en.wikipedia.org/wiki/Busy_waiting) polling operation on the Selenium `wait` operation (defaults to `None`). |
| **RIPE_ID_USERNAME** | `str` | The username to be used for the RIPE ID authentication (defaults to `None` ) |
| **RIPE_ID_PASSWORD** | `str` | The password to be used for the RIPE ID authentication (defaults to `None` ) |

## License

RIPE Rainbow is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/ripe-tech/ripe-rainbow.svg?branch=master)](https://travis-ci.org/ripe-tech/ripe-rainbow)
[![Coverage Status](https://coveralls.io/repos/ripe-tech/ripe-rainbow/badge.svg?branch=master)](https://coveralls.io/r/ripe-tech/ripe-rainbow?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/ripe-rainbow.svg)](https://pypi.python.org/pypi/ripe-rainbow)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
