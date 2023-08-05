#!/usr/bin/env python
"""Setup script"""

from setuptools import setup, find_packages

description = """
This module does nothing, but is useful when trying to build documentation
for modules that require wxPython.

Do not install this module if you already have wxPython installed, as it uses
the same "wx" package name to pretend to be wxPython.

"""

setup(
    author="Dominic Davis-Foster",
    author_email="dominic@davis-foster.co.uk",
    description="This module does nothing",
    license="LGPLv3+",
    long_description=description,
    name="dummy_wx",
    packages=find_packages(),
    version="0.2.4",
    )
