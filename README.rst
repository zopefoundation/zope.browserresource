======================
 zope.browserresource
======================

.. image:: https://img.shields.io/pypi/v/zope.browserresource.svg
        :target: https://pypi.python.org/pypi/zope.browserresource/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.browserresource.svg
        :target: https://pypi.org/project/zope.browserresource/
        :alt: Supported Python versions

.. image:: https://github.com/zopefoundation/zope.browserresource/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/zope.browserresource/actions/workflows/tests.yml

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.browserresource/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.browserresource?branch=master

.. image:: https://readthedocs.org/projects/zopebrowserresource/badge/?version=latest
        :target: https://zopebrowserresource.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. note::
   This package is at present not reusable without depending on a large
   chunk of the Zope Toolkit and its assumptions. It is maintained by the
   `Zope Toolkit project <http://docs.zope.org/zopetoolkit/>`_.

This package provides an implementation of browser resources. It also
provides directives for defining those resources using ZCML.

Resources are static files and directories that are served to the browser
directly from the filesystem. The most common example are images, CSS style
sheets, or JavaScript files.

Resources are be registered under a symbolic name and can later be referred to
by that name, so their usage is independent from their physical
location. Resources can also easily be internationalized.

Documentation is hosted at https://zopebrowserresource.readthedocs.io
