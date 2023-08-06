#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (C) 2017 David Toro <davsamirtor@gmail.com>

# import build-in modules
import io
import os
import re

__author__ = "David Toro"
__license__ = "BSD-3-Clause"
__maintainer__ = "David Toro"
__email__ = "davsamirtor@gmail.com"


def read(*names, **kwargs):
    """Python 2 and Python 3 compatible text file reading.
    Required for single-sourcing the version string.
    """
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    """
    Search the file for a version string.
    file_path contain string path components.
    Reads the supplied Python module as text without importing it.
    """
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

current_path = os.path.abspath(os.path.dirname(__file__))