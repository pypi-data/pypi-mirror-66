#!/usr/bin/env python3
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as file:
    readme = file.read()

# Setup
setup(
    name='dnassembly',
    version='0.1.3',
    author='James Lucas',
    author_email='james.lucas@berkeley.edu',
    description='',
    long_description=readme,
    url='https://github.com/jaaamessszzz/DNAssembly',
    keywords=[
        'DNA',
        'assembly',
        'cloning'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    packages=[
        'dnassembly',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    include_package_data=True,
    zip_safe=False,
)