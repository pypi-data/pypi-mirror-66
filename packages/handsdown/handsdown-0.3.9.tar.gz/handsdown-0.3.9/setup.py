#!/usr/bin/env python
"""
Handsdown setup module for `setuptools`.
"""
import os
import sys

from setuptools import setup
from setuptools import find_packages
from handsdown.version import version


if sys.version_info < (3, 5, 0):
    sys.stderr.write("ERROR: You need Python 3.5 or later to use handsdown.\n")
    sys.exit(1)

root_path = os.path.dirname(os.path.abspath(__file__))

description = "Python docstring-based documentation generator for lazy perfectionists."


def get_long_description():
    """
    Remove ToC from README.md as PyPI does not support links.
    """
    lines = []
    readme_path = os.path.join(root_path, "README.md")
    with open(readme_path) as readme_file:
        for readme_line in readme_file.readlines():
            if "](#" not in readme_line:
                lines.append(readme_line.rstrip("\n"))
    return "\n".join(lines)


def get_install_requires():
    """
    Parse requirements from `requirements.txt`.
    """
    install_requires = []
    requirements_path = os.path.join(root_path, "requirements.txt")
    with open(requirements_path) as f:
        for line in f.readlines():
            line = line.rstrip(" \n")
            if line:
                install_requires.append(line)

    return install_requires


long_description = get_long_description()


setup(
    name="handsdown",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://vemel.github.io/handsdown/",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    packages=find_packages(
        exclude=["tests", "tests.*", "__pycache__", "examples", "examples.*"]
    ),
    install_requires=get_install_requires(),
    extras_require={},
    package_data={"handsdown": ["handsdown/assets/*.yml"]},
    include_package_data=True,
    zip_safe=True,
    dependency_links=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    entry_points={"console_scripts": ["handsdown = handsdown.main:main"]},
    project_urls={
        "Source": "https://github.com/vemel/handsdown/",
        "Documentation": "https://vemel.github.io/handsdown/",
    },
)
