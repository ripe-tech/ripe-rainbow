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

| Name | Type | Default | Description |
| ----- | ----- | ----- | ----- |
| **LEVEL** | `str` | `INFO` | Controls the verbosity level of the attached logger. |
| **SILENT** | `bool` | `False` | If the test execution should run under silent mode (no stdout from logs). |
| **FILTER** | `str` | `None` | The filter regex to be used by some of the loaders. |
| **DRIVER** | `str` | `selenium` | The driver to be used for the interactive mode. |
| **TIMEOUT** | `int` | `15` | The timeout in seconds to be used by default for interactions under the interactive testing mode. |
| **REPEAT** | `int` | `1` | The number of times to repeat the execution of the tests. |
| **PROVISION** | `bool` | `True` | If the provision operations should be performed. |
| **STACKTRACES** | `bool` | `False` | If "stacktrace" log should be stored on failure of tests. |
| **STACKTRACES_PATH** | `bool` | `.` | The base path to be used to save the stacktraces log. |
| **SCREENSHOTS** | `bool` | `False` | If screenshots should be save on failure of tests. |
| **SCREENSHOTS_PATH** | `bool` | `.` | The base path to be used to save the screenshots. |
| **STORE_LOGS** | `bool` | `False` | If the log files from the multiple logs should be store in case of test failure. |
| **LOGS_PATH** | `bool` | `.` | The base path to be used to save the log files on failure. |
| **SEL_SECURE** | `bool` | `False` | If the [Selenium](https://www.seleniumhq.org) engine should be executed under a secure approach (should be slower). |
| **SEL_BROWSER** | `str` | `chrome` | The browser engine that is going to be used by Selenium (eg: `chrome`, `firefox`). |
| **SEL_BROWSER_CACHE** | `bool` | `True` | If the [Selenium](https://www.seleniumhq.org) driver should be with browser cache enabled. |
| **SEL_MAXIMIZED** | `bool` | `False` | If the [Selenium](https://www.seleniumhq.org) driver should be started in "maximized" (window) mode. |
| **SEL_HEADLESS** | `bool` | `False` | If the [Selenium](https://www.seleniumhq.org) driver should be started in "headless" (window) mode. |
| **SEL_WINDOW_SIZE** | `str` | `1920x1080` | Resolution (in pixels) that the [Selenium](https://www.seleniumhq.org) driver will use for the window. |
| **SEL_SERVICE_ARGS** | `list` | `[]` | List of command line args to be passed to the driver service that interacts with the browser. |
| **SEL_POLL_FREQUENCY** | `float` | `None` | The frequency (in seconds) to run the [busy waiting](https://en.wikipedia.org/wiki/Busy_waiting) polling operation on the Selenium `wait` operation. |
| **RIPE_ID_USERNAME** | `str` | `None` | The username to be used for the RIPE ID authentication. |
| **RIPE_ID_PASSWORD** | `str` | `None` | The password to be used for the RIPE ID authentication. |

| Name | Type | Default |  Description |
| ----- | ----- | ----- | ----- |
| **RIPE_SUFFIX** | `str` | `None` | If defined the RIPE product URLs are suffixed with this value (eg: `sbx` implies `https://ripe-pulse-sbx.platforme.com`). |
| **RIPE_CORE_URL** | `str` | `http://localhost:8080` | The base URL to the RIPE Core instance to be used for tests. |
| **CORE_URL** | `str` | `http://localhost:8080` | Same as `RIPE_CORE_URL`. |
| **RIPE_CORE_USERNAME** | `str` | `root` | The username of an admin user to be used to access RIPE Core, it is also used in the provision operation. |
| **CORE_USERNAME** | `str` | `root` | Same as `RIPE_CORE_USERNAME`. |
| **RIPE_CORE_PASSWORD** | `str` | `root` | The password of an admin user to be used to access RIPE Core, it is also used in the provision operation. |
| **CORE_PASSWORD** | `str` | `root` | Same as `RIPE_CORE_PASSWORD`. |
| **RIPE_RETAIL_URL** | `str` | `http://localhost:8080` | The base URL to the RIPE Retail instance to be used for tests. |
| **RETAIL_URL** | `str` | `http://localhost:8080` | Same as `RIPE_RETAIL_URL`. |
| **RIPE_RETAIL_USERNAME** | `str` | `root` | The username of an admin user to be used to access RIPE Retail, it is also used in the provision operation. |
| **RETAIL_USERNAME** | `str` | `root` | Same as `RIPE_RETAIL_USERNAME`. |
| **RIPE_RETAIL_PASSWORD** | `str` | `root` | The password of an admin user to be used to access RIPE Retail, it is also used in the provision operation. |
| **RETAIL_PASSWORD** | `str` | `root` | Same as `RIPE_RETAIL_PASSWORD`. |
| **RETAIL_URL** | `str` | `http://localhost:8080` | Same as `RIPE_RETAIL_URL`. |
| **RIPE_PULSE_URL** | `str` | `http://localhost:3000` | The base URL to the RIPE Pulse instance to be used for tests. |
| **PULSE_URL** | `str` | `http://localhost:3000` | Same as `RIPE_PULSE_URL`. |
| **RIPE_COPPER_URL** | `str` | `http://localhost:3000` | The base URL to the RIPE Copper instance to be used for tests. |
| **COPPER_URL** | `str` | `http://localhost:3000` | Same as `RIPE_COPPER_URL`. |
| **RIPE_WHITE_URL** | `str` | `http://localhost:3000` | The base URL to the RIPE White instance to be used for tests. |
| **WHITE_URL** | `str` | `http://localhost:3000` | Same as `RIPE_WHITE_URL`. |

## License

RIPE Rainbow is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/ripe-tech/ripe-rainbow.svg?branch=master)](https://travis-ci.org/ripe-tech/ripe-rainbow)
[![Coverage Status](https://coveralls.io/repos/ripe-tech/ripe-rainbow/badge.svg?branch=master)](https://coveralls.io/r/ripe-tech/ripe-rainbow?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/ripe-rainbow.svg)](https://pypi.python.org/pypi/ripe-rainbow)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
