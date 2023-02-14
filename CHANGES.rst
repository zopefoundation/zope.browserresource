=========
 Changes
=========

5.0 (2023-02-14)
================

- Drop support for Python 2.7, 3.5, 3.6.

- Add support for Python 3.9, 3.10, 3.11.

- Drop support for ``python setup.py test``.


4.4 (2019-12-10)
================

- Make the registration of the ``FileETag`` adapter conditional on the environment
  as Zope 4 registers this adapter explicitly in ``Products.Five.browser``.
  See `#12 <https://github.com/zopefoundation/zope.browserresource/pull/12>`_.

- Add support for Python 3.8.

- Drop support for Python 3.4.


4.3 (2018-10-05)
================

- Add support for Python 3.7.

- Host documentation at https://zopebrowserresource.readthedocs.io

- Add ``.git`` to the list of directory names that are ignored by default.

- Fix test compatibility with zope.i18n 4.3.
  See `#8 <https://github.com/zopefoundation/zope.browserresource/issues/8>`_


4.2.1 (2017-09-01)
==================

- Fix dependencies of the ``zcml`` extra.


4.2.0 (2017-08-04)
==================

- Add support for Python 3.5 and 3.6.

- Drop support for Python 2.6 and 3.3.


4.1.0 (2014-12-26)
==================

- Add support for PyPy.  PyPy3 support awaits release of fix for:
  https://bitbucket.org/pypy/pypy/issue/1946

- Add support for Python 3.4.

- Add support for testing on Travis.


4.0.2 (2014-11-04)
==================

- Return no ETag if no adapter is registered, disabling the
  requirement for applications that was introduced in 3.11.0 (GitHub #1)


4.0.1 (2013-04-03)
==================

- Fix some Python 3 string vs bytes issues.


4.0.0 (2013-02-20)
==================

- Replace deprecated `zope.component.adapts` usage with equivalent
  `zope.component.adapter` decorator.

- Replace deprecated `zope.interface.classProvides` usage with equivalent
  `zope.interface.provider` decorator.

- Replace deprecated `zope.interface.implementsOnly` usage with equivalent
  `zope.interface.implementer_only` decorator.

- Replace deprecated `zope.interface.implements` usage with equivalent
  `zope.interface.implementer` decorator.

- Drop support for Python 2.4 and 2.5.

- Add support for Python 3.3.


3.12.0 (2010-12-14)
===================

- Add ``zcml`` extra dependencies and fixed dependencies of
  ``configure.zcml`` on other packages' ``meta.zcml``.

- Add a test for including our own ``configure.zcml``.

3.11.0 (2010-08-13)
===================

- Support the HTTP ETag header for file resources.  ETag generation can be
  customized or disabled by providing an IETag multi-adapter on
  (IFileResource, your-application-skin).

3.10.3 (2010-04-30)
===================

- Prefer the standard libraries doctest module to the one from zope.testing.

3.10.2 (2009-11-25)
===================

- The previous release had a broken egg, sorry.

3.10.1 (2009-11-24)
===================

- Import hooks functionality from zope.component after it was moved there from
  zope.site. This lifts the dependency on zope.site and thereby, ZODB.

- Import ISite and IPossibleSite from zope.component after they were moved
  there from zope.location.

3.10.0 (2009-09-25)
===================

- Add an ability to forbid publishing of some files in the resource directory,
  this is done by fnmatch'ing the wildcards in the ``forbidden_names``class
  attribute of ``DirectoryResource``. By default, the ``.svn`` is in that
  attribute, so directories won't publish subversion system directory that can
  contain private information.

3.9.0 (2009-08-27)
==================

Initial release. This package was splitted off zope.app.publisher as a part
of refactoring process.

Additional changes that are made during refactoring:

 * Resource class for file resources are now selected the pluggable way.
   The resource directory publisher and browser:resource ZCML directive
   now creating file resources using factory utility lookup based on the
   file extension, so it's now possible to add new resource types without
   introducing new ZCML directives and they will work inside resource
   directories as well.

   NOTE: the "resource_factories" attribute from the DirectoryResource
   was removed, so if you were using this attribute for changing resource
   classes for some file extensions, you need to migrate your code to new
   utility-based mechanism.

   See zope.browserresource.interfaces.IResourceFactoryFactory interface.

 * The Image resource class was removed, as they are actually simple files.
   To migrate, simply rename the "image" argument in browser:resource and
   browser:i18n-resource directives to "file", if you don't do this, resouces
   will work, but you'll get deprecation warnings.

   If you need custom behaviour for images, you can register a resource
   factory utility for needed file extensions.

 * The PageTemplateResource was moved into a separate package, "zope.ptresource",
   which is a plugin for this package now. Because of that, the "template"
   argument of browser:resource directive was deprecated and you should rename
   it to "file" to migrate. The PageTemplateResource will be created for
   "pt", "zpt" and "html" files automatically, if zope.ptresource package is
   included in your configuration.

 * Fix stripping the "I" from an interface name for icon title, if no
   title is specified.

 * When publishing a resource via Resources view, set resource parent
   to an ISite object, not to current site manager.

 * Clean up code and improve test coverage.
