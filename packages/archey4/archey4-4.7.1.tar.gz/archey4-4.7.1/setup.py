#!/usr/bin/env python3

"""
This is the Archey 4's `setup.py` file, allowing us to distribute it as a package...
... with cool meta-data.
"""

from setuptools import find_packages, setup

from archey._version import __version__


setup(
    name='archey4',
    version=__version__.lstrip('v'),
    description='Archey is a simple system information tool written in Python',
    keywords='archey python3 linux system-information monitoring',
    url='https://github.com/HorlogeSkynet/archey4',
    author='Samuel FORESTIER',  # Not alone
    author_email='dev+archey@samuel.domains',
    license='GPLv3',
    packages=find_packages(exclude=['archey.test']),
    test_suite='archey.test',
    install_requires=[
        'distro',
        'netifaces'
    ],
    entry_points={
        'console_scripts': [
            'archey = archey.__main__:main'
        ]
    },
    long_description='Maintained fork of the original Archey Linux system tool'
                     ' originally written by Melik Manukyan.',
    long_description_content_type='text/plain',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System'
    ]
)
