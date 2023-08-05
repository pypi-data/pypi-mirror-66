#!/usr/bin/python
# -*- coding:utf-8 -*-
# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages
import os
import sys


# Get description from Readme file
readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(readme_file).read()


setup(name='random_timestamp',
      version='1.0.1',
      description='A Random Timestamp Generator',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='FENG Hao',
      author_email='hiroshifuu@outlook.com',
      url='https://github.com/HiroshiFuu/random_timestamp',
      download_url='https://pypi.python.org/pypi/random_timestamp',
      license='GPL v3.0',
      packages=['random_timestamp'],
      include_package_data=True,
      keywords='random date time timestamp',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 3',
              'Environment :: Console',
              'Natural Language :: English',
              'Intended Audience :: Developers',
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'random_timestamp=random_timestamp.__main__:main',
          ]
      },
      )
