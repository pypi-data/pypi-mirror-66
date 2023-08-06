"""setup.py

The setup script of TMJ.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
from os import path
from setuptools import setup

here = path.join(path.dirname(__file__))


def get_repo_file_content(filename: str) -> str:
    with open(path.join(here, filename), encoding="utf-8") as f:
        return f.read()


setup(
    name="tmj",
    version="v1.0.0",
    description=
    "Small CLI utility script to help me with TMJ disorder isometric jaw exercises.",
    long_description=get_repo_file_content("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/Figglewatts/tmj",
    author="Figglewatts",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console", "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7", "Topic :: Utilities",
        "Typing :: Typed"
    ],
    keywords="tmj temporomandibular joint disorder",
    python_requires=">=3.7",
    install_requires=["colorama>=0.4.3"],
    entry_points={"console_scripts": ["tmj=tmj:main"]},
    py_modules=["tmj"])
