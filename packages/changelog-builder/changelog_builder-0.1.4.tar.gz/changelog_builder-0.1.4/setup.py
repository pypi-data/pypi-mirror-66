#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-04-21"
__version__ = "0.1.4"

__all__ = ()

from pathlib import Path
from setuptools import setup, find_packages

if __name__ == '__main__':
    with Path('README.md').open('r') as file: long_description = file.read()
    with Path('requirements.txt').open('r') as file:
        requirements = [r.split('=')[0].rstrip('~<>=')
                        for r in file.read().splitlines()
                        if not (r.startswith('#') or r == '' or r == '\n')]
    setup(
        name='changelog_builder',
        version=__version__,
        packages=find_packages(),
        url='https://github.com/RoW171/changelog_builder',
        license='MIT',
        author=__author__,
        author_email='robin.weiland@gmx.de',
        description='Tool for creating changelogs',
        long_description=long_description,
        long_description_content_type='text/markdown',
        keywords=['changelog', 'change', 'log'],
        requires=requirements,
        python_requires='>=3.5',
        py_modules=['changelog_builder'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Operating System :: OS Independent',
        ],
        entry_points={
            'console_scripts': [
                'changelog-builder = changelog_builder:main'
            ]
        }
    )
