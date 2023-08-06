#!/usr/bin/env python

import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('hoof.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='hoof',
    version=version,
    py_modules=['hoof'],
    install_requires=['antlr4-python3-runtime'],
    description='Generate abstract syntax trees using antlr grammars',
    author='Michael Chow',
    author_email='mc_al_github@fastmail.com',
    url='https://github.com/machow/hoof'
    )
