##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""zope.browserresource setup
"""
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = read('README.rst') + '\n\n' + read('CHANGES.rst')

ZCML_REQUIRES = [
    'zope.component[zcml]',
    'zope.security[zcml] >= 3.8',
]

TESTS_REQUIRE = ZCML_REQUIRES + [
    'zope.testing',
    'zope.testrunner',
]

setup(name='zope.browserresource',
      version='5.0',
      url='https://github.com/zopefoundation/zope.browserresource/',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.dev',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      description='Browser resources implementation for Zope.',
      long_description=long_description,
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope'],
      include_package_data=True,
      python_requires='>=3.7',
      install_requires=[
          'setuptools',
          'zope.component>=3.8.0',
          'zope.configuration',
          'zope.contenttype>=4.0.1',
          'zope.i18n',
          'zope.interface',
          'zope.location',
          'zope.publisher>=3.8',
          'zope.schema',
          'zope.traversing>3.7',
      ],
      extras_require={
          'test': TESTS_REQUIRE,
          'zcml': ZCML_REQUIRES,
          'docs': [
              'Sphinx',
              'repoze.sphinx.autointerface',
          ],
      },
      zip_safe=False)
