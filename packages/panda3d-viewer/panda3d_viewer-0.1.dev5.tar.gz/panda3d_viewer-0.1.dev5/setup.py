#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

__version__ = '0.1'

if 'TRAVIS_BUILD_NUMBER' in os.environ and 'TRAVIS_BRANCH' in os.environ:
    # TRAVIS-CI build
    travis_branch = os.environ['TRAVIS_BRANCH']
    travis_build = os.environ['TRAVIS_BUILD_NUMBER']
    is_release = 'release' in travis_branch or 'master' == travis_branch

    dev_status = '5 - Production/Stable' if is_release else '4 - Beta'
    __version__ += '.{}{}'.format('' if is_release else 'dev', travis_build)
else:
    # local build
    dev_status = '4 - Beta'
    __version__ += '.dev5'

install_requires = ['numpy', 'panda3d']

setup(name='panda3d_viewer',
      version=__version__,
      description='Easy-to-use Python Panda3D-based 3D graphics viewer',
      long_description='You can find detailed manual here: https://github.com/ikalevatykh/panda3d_viewer',
      url='https://github.com/ikalevatykh/panda3d_viewer',
      download_url='https://github.com/ikalevatykh/panda3d_viewer',
      author='Igor Kalevatykh',
      license='Modified BSD License',
      classifiers=[
          'Development Status :: {}'.format(dev_status),
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
      ],
      keywords='rendering graphics 3d visualization',
      packages=find_packages(),
      install_requires=install_requires,
      package_data={'': ['LICENSE', 'README.md']},
      zip_safe=True)
