==========
 Overview
==========

.. highlight:: xml

This package provides an implementation of browser resources. It also
provides directives for defining those resources using ZCML.

Resources are static files and directories that are served to the
browser directly from the filesystem. The most common example are
images, CSS style sheets, or JavaScript files.

Resources are be registered under a symbolic name and can later be
referred to by that name, so their usage is independent from their
physical location.

Registering Resources
=====================

You can register a single file with the ``<browser:resource>``
directive, and a whole directory with the
``<browser:resourceDirectory>`` directive, for example::

  <browser:resource
    file="/path/to/static.file"
    name="myfile"
    />

  <browser:resourceDirectory
    directory="/path/to/images"
    name="main-images"
    />

This causes a named default adapter to be registered that adapts the
*request* to :class:`zope.interface.Interface` so to later retrieve a
resource, use ``zope.component.getAdapter(request, name='myfile')``.

.. note::
   The default adapter (the one that adapts to
   :class:`zope.interface.Interface`) is used to reduce
   coupling between projects, specifically between this project
   and `zope.traversing.namespace`.

Internationalization
====================

Resources can also be internationalized, which means that a single
resource name can refer to any one of a number of files that are
specific to different languages. When the resource is retrieved and
served, the file that corresponds to the request's language is
automatically sent::

  <browser:i18n-resource
    name="myfile"
    defaultLanguage="en">
    <browser:translation
      language="en"
      file="path/to/static.file"
      />
    <browser:translation
      language="de"
      file="path/to/static.file.de"
      />
  </browser:i18n-resource>

Using Resources
===============

There are two ways to traverse to a resource:

1. with the 'empty' view on a site, e. g. ``http://localhost/@@/myfile``
   (This is declared by ``zope.browserresource``'s ``configure.zcml``
   to be `.Resources`.)

2. with the ``++resource++`` namespace, e. g. ``http://localhost/++resource++myfile``
   (This is declared by `zope.traversing.namespace`)

In case of resource-directories traversal simply continues through its
contents,
e. g. ``http://localhost/@@/main-images/subdir/sample.jpg``

Rather than putting together the URL to a resource manually, you should use
`zope.traversing.browser.interfaces.IAbsoluteURL` to get the URL, or for a
shorthand, call the resource object. This has an additional benefit:

If you want to serve resources from a different URL, for example
because you want to use a web server specialized in serving static
files instead of the appserver, you can register an ``IAbsoluteURL``
adapter for the site under the name ``resource`` that will be used to
compute the base URLs for resources. (See `.AbsoluteURL` for the
implementation.)

For example, if you register ``http://static.example.com/`` as the
base ``resource`` URL, the resources from the above example would yield
the following absolute URLs: ``http://static.example.com/@@/myfile``
and ``http://static.example.com/@@/main-images``.
