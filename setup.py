# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


setup(
    name='pyoxy',
    description='Python object proxy',
    version='0.1.dev0',
    url='https://github.com/jacekmitrega/pyoxy',
    author='Jacek Mitręga',
    license='Apache License, Version 2.0',
    install_requires=open('requirements.txt').read(),
    packages=find_packages(),
    zip_safe=True,
)
