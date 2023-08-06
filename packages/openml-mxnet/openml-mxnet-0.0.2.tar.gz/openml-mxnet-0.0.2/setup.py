# -*- coding: utf-8 -*-

# License: BSD 3-Clause

import os
import setuptools
import sys

if sys.version_info < (3, 5):
    raise ValueError(
        'Unsupported Python version {}.{}.{} found. OpenML requires Python 3.5 or higher.'
        .format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    )

with open(os.path.join("README.md")) as fid:
    README = fid.read()

setuptools.setup(name="openml-mxnet",
                 version = "0.0.2",
                 author=" ",
                 author_email="",
                 maintainer="Prabhant Singh",
                 maintainer_email="prabhantsingh@gmail.com",
                 description="MXNet extension for Openml python API",
                 long_description=README,
                 long_description_content_type='text/markdown',
                 license="BSD 3-clause",
                 url="http://openml.org/",
                 project_urls={
                     "Documentation": "https://openml.github.io/openml-mxnet/",
                     "Source Code": "https://github.com/openml/openml-mxnet"
                 },
                 # Make sure to remove stale files such as the egg-info before updating this:
                 # https://stackoverflow.com/a/26547314
                 packages=setuptools.find_packages(
                     include=['openml_mxnet.*', 'openml_mxnet'],
                     exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
                 ),
                 package_data={'': ['*.txt', '*.md']},
                 python_requires=">=3.5",
                 install_requires=[
                     'openml',
                     'mxnet>=1.4.1'
                 ],
                 classifiers=['Intended Audience :: Science/Research',
                              'Intended Audience :: Developers',
                              'License :: OSI Approved :: BSD License',
                              'Programming Language :: Python',
                              'Topic :: Software Development',
                              'Topic :: Scientific/Engineering',
                              'Operating System :: POSIX',
                              'Operating System :: Unix',
                              'Operating System :: MacOS',
                              'Programming Language :: Python :: 3',
                              'Programming Language :: Python :: 3.5',
                              'Programming Language :: Python :: 3.6',
                              'Programming Language :: Python :: 3.7'])