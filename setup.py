#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='wonderland',
    version="0.0.0",
    author="Peilonrayz",
    zip_safe=False,
    install_requires=["Sphinx", "docutils", "kecleon", "beautifulsoup4"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    # entry_points={"console_scripts": ["cr=cr.__main__:main"]},
)
