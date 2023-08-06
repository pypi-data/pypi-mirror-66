#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import codecs
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme_md = os.path.join(here, 'README.md')

# Get the package description from the README.md file
with codecs.open(readme_md, encoding='utf-8') as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mcthings_drawing',
    version='0.0.2',
    packages=['mcthings_drawing'],
    include_package_data=True,
    license='ASL',
    description='McThings Extension for building things in Minecraft with MinecraftDrawings',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/juntosdesdecasa/mcthings_drawing',
    author='Alvaro del Castillo',
    author_email='alvaro.delcastillo@gmail.com',
    keywords="development library minecraft buildings games python",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'
    ],
    install_requires=[
        'mcpi',
        'mcthings >= 0.5.3',
        'minecraftstuff'
    ],
    python_requires='>=3.4'
)
