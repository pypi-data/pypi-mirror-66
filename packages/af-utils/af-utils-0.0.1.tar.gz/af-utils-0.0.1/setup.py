# -*- coding: utf-8 -*-
# Airflow Utilis (af-utils)

# Authors: Lee Ying Yang <overaneout@gmail.com>

from setuptools import setup, find_packages

with open("README.md","r") as fh:
  long_desc = fh.read()

setup(
  name="af-utils",
  version="0.0.1",
  author="Lee Ying Yang",
  author_email="overaneout@gmail.com",
  description="airflow utilities for an internal package",
  long_description=long_desc,
  long_description_content_type="text/markdown",
  license="Apache Software License (Apache License 2.0)",
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False
)