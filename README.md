# RIPE Rainbow

**Bringing happiness to the RIPE world through testing 🌈**

RIPE Rainbow is a simple automation test framework for the RIPE world.

## Installation

```bash
pip install ripe-rainbow
```

## Execution

```bash
ripe-rainbow
```

### Selecting tests

It's also possible to run only certain tests. To do so, you can use `rainbow ${REGEX}`, where the regex will be tested against `file_name:test_class:test_method` (e.g.: `account_login.AccountLoginTest.invalid_empty_login`) and the test will only run if it passes.

For instance, if you want to run all the tests in `AccountLoginTest` you can `rainbow .*AccountLoginTest.*`.

## License

RIPE Rainbow is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://travis-ci.org/ripe-tech/ripe-rainbow.svg?branch=master)](https://travis-ci.org/ripe-tech/ripe-rainbow)
[![Coverage Status](https://coveralls.io/repos/ripe-tech/ripe-rainbow/badge.svg?branch=master)](https://coveralls.io/r/ripe-tech/ripe-rainbow?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/ripe-rainbow.svg)](https://pypi.python.org/pypi/ripe-rainbow)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
