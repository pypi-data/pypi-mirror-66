# -*- coding: utf-8 -*-


import setuptools

import pathlib
import os

pathlib.Path(__file__).parent.absolute()

with open(os.path.join(pathlib.Path(__file__).parent.absolute(), 'VERSION.txt')) as version_file:
    version = version_file.read().strip()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fgp',
    version=version,
    author='Future Grid',
    author_email='team@future-grid.com',
    description='Future Grid API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[                      # Add project dependencies here
        'pytest',
        'requests'
    ],
    url='https://gitlab.com/future-grid/fgp-api-python',
    packages=setuptools.find_packages(),
    package_data={'fgp': ['VERSION.txt']},
    include_package_data=True,
    classifiers=(                                 # Classifiers help people find your
        'Programming Language :: Python :: 3',    # projects. See all possible classifiers
        'License :: OSI Approved :: MIT License', # in https://pypi.org/classifiers/
        'Operating System :: OS Independent',
    ),
    data_files=[('', ['VERSION.txt'])]
    # entry_points={
    #     'console_scripts': [
    #         "nml=nml:cli"
    #     ]
    # }
)
