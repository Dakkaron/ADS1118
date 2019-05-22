#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = ['Development Status :: 5 - Production/Stable',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(
    name='ads1118',
    version='1.1',
    author='David Krywult',
    author_email='dak1st@gmx.at',
    description="""Python library for the ADS1118 4-channel ADC""",
    long_description=open('README.md').read(),
    license='MIT',
    keywords='Raspberry Pi',
    classifiers=classifiers,
    packages=['ads1118'],
    install_requires=['spidev>=3.4']
)
