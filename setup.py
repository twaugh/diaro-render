#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name="diaro-render",
    description='Render Diaro data files into HTML',
    version="0.1",
    author='Tim Waugh',
    author_email='tim@cyberelk.net',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
          'console_scripts': ['diaro-render=diaro_render.cli.main:main'],
    },
)
