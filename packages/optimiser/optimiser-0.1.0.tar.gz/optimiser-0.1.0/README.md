[![Build Status](https://travis-ci.org/Nikolay-Lysenko/optimiser.svg?branch=master)](https://travis-ci.org/Nikolay-Lysenko/optimiser)
[![codecov](https://codecov.io/gh/Nikolay-Lysenko/optimiser/branch/master/graph/badge.svg)](https://codecov.io/gh/Nikolay-Lysenko/optimiser)
[![Maintainability](https://api.codeclimate.com/v1/badges/1ef4e3ac74a4d7ed2291/maintainability)](https://codeclimate.com/github/Nikolay-Lysenko/optimiser/maintainability)
[![PyPI version](https://badge.fury.io/py/optimiser.svg)](https://badge.fury.io/py/optimiser)


# Optimiser

## Overview

This Python package is a library with implementations of some optimization techniques. Current content is shown in the below table:

Method | Implementation
:----: | :------------:
[Cross-Entropy](https://github.com/Nikolay-Lysenko/optimiser/blob/master/docs/crossentropy.pdf) | [optimize_with_crossentropy_method](https://github.com/Nikolay-Lysenko/optimiser/blob/master/optimiser/population/crossentropy.py)

Of course, just one function is not that much...

## Installation

```bash
pip install optimiser
```

## Usage

All functions from the package (especially, those of them that are designed for end users) have a built-in documentation that describes every argument. To read it, look at a docstring or, alternatively, run from Python shell a command like this one:
```python
help(optimize_with_crossentropy_method)
```
