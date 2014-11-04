##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""File-based browser resource tests.
"""

import doctest
import os
import re
import unittest
import time
try:
    from email.utils import formatdate, parsedate_tz, mktime_tz
except ImportError: # python 2.4
    from email.Utils import formatdate, parsedate_tz, mktime_tz

from zope.testing import cleanup
from zope.testing.renormalizing import RENormalizing
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.security.checker import NamesChecker
from zope.component import provideAdapter, adapter, getGlobalSiteManager
from zope.interface import implementer
from zope.interface.verify import verifyObject

from zope.browserresource.file import FileResourceFactory, FileETag
from zope.browserresource.interfaces import IFileResource, IETag


@adapter(IFileResource, IBrowserRequest)
@implementer(IETag)
class MyETag(object):

    def __init__(self, context, request):
        pass

    def __call__(self, mtime, content):
        return 'myetag'


@adapter(IFileResource, IBrowserRequest)
@implementer(IETag)
class NoETag(object):

    def __init__(self, context, request):
        pass

    def __call__(self, mtime, content):
        return None


def setUp(test):
    cleanup.setUp()
    data_dir = os.path.join(os.path.dirname(__file__), 'testfiles')

    test.globs['testFilePath'] = os.path.join(data_dir, 'test.txt')
    test.globs['nullChecker'] = NamesChecker()
    test.globs['TestRequest'] = TestRequest
    provideAdapter(MyETag)


def tearDown(test):
    cleanup.tearDown()


def doctest_FileETag():
    """Tests for FileETag

        >>> etag_maker = FileETag(object(), TestRequest())
        >>> verifyObject(IETag, etag_maker)
        True

    By default we constuct an ETag from the file's mtime and size

        >>> etag_maker(1234, 'abc')
        '1234-3'

    """


def doctest_FileResource_GET_sets_cache_headers():
    """Test caching headers set by FileResource.GET

        >>> factory = FileResourceFactory(testFilePath, nullChecker, 'test.txt')

        >>> timestamp = time.time()

        >>> file = factory._FileResourceFactory__file # get mangled file
        >>> file.lmt = timestamp
        >>> file.lmh = formatdate(timestamp, usegmt=True)

        >>> request = TestRequest()
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

        >>> request.response.getHeader('Last-Modified') == file.lmh
        True
        >>> request.response.getHeader('ETag')
        '"myetag"'
        >>> request.response.getHeader('Cache-Control')
        'public,max-age=86400'
        >>> bool(request.response.getHeader('Expires'))
        True

    """


def doctest_FileResource_GET_if_modified_since():
    """Test If-Modified-Since header support

        >>> factory = FileResourceFactory(testFilePath, nullChecker, 'test.txt')

        >>> timestamp = time.time()

        >>> file = factory._FileResourceFactory__file # get mangled file
        >>> file.lmt = timestamp
        >>> file.lmh = formatdate(timestamp, usegmt=True)

        >>> before = timestamp - 1000
        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(before, usegmt=True))
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

        >>> after = timestamp + 1000
        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(after, usegmt=True))
        >>> resource = factory(request)
        >>> bool(resource.GET())
        False
        >>> request.response.getStatus()
        304

    Cache control headers and ETag are set on 304 responses

        >>> request.response.getHeader('ETag')
        '"myetag"'
        >>> request.response.getHeader('Cache-Control')
        'public,max-age=86400'
        >>> bool(request.response.getHeader('Expires'))
        True

    Other entity headers are not

        >>> request.response.getHeader('Last-Modified')
        >>> request.response.getHeader('Content-Type')

    It won't fail on bad If-Modified-Since headers.

        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE='bad header')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    it also won't fail if we don't have a last modification time for the
    resource

        >>> file.lmt = None
        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(after, usegmt=True))
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    """


def doctest_FileResource_GET_if_none_match():
    """Test If-None-Match header support

        >>> factory = FileResourceFactory(testFilePath, nullChecker, 'test.txt')

        >>> timestamp = time.time()

        >>> file = factory._FileResourceFactory__file # get mangled file
        >>> file.lmt = timestamp
        >>> file.lmh = formatdate(timestamp, usegmt=True)

        >>> request = TestRequest(HTTP_IF_NONE_MATCH='"othertag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

        >>> request = TestRequest(HTTP_IF_NONE_MATCH='"myetag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        False
        >>> request.response.getStatus()
        304

    Cache control headers and ETag are set on 304 responses

        >>> request.response.getHeader('ETag')
        '"myetag"'
        >>> request.response.getHeader('Cache-Control')
        'public,max-age=86400'
        >>> bool(request.response.getHeader('Expires'))
        True

    Other entity headers are not

        >>> request.response.getHeader('Last-Modified')
        >>> request.response.getHeader('Content-Type')

    It won't fail on bad If-None-Match headers.

        >>> request = TestRequest(HTTP_IF_NONE_MATCH='bad header')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    it also won't fail if we don't have an etag for the resource

        >>> provideAdapter(NoETag)
        >>> request = TestRequest(HTTP_IF_NONE_MATCH='"someetag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    """


def doctest_FileResource_GET_if_none_match_and_if_modified_since():
    """Test combined If-None-Match and If-Modified-Since header support

        >>> factory = FileResourceFactory(testFilePath, nullChecker, 'test.txt')

        >>> timestamp = time.time()

        >>> file = factory._FileResourceFactory__file # get mangled file
        >>> file.lmt = timestamp
        >>> file.lmh = formatdate(timestamp, usegmt=True)

    We've a match

        >>> after = timestamp + 1000
        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(after, usegmt=True),
        ...                       HTTP_IF_NONE_MATCH='"myetag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        False
        >>> request.response.getStatus()
        304

    Last-modified matches, but ETag doesn't

        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(after, usegmt=True),
        ...                       HTTP_IF_NONE_MATCH='"otheretag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    ETag matches but last-modified doesn't

        >>> before = timestamp - 1000
        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(before, usegmt=True),
        ...                       HTTP_IF_NONE_MATCH='"myetag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    Both don't match

        >>> before = timestamp - 1000
        >>> request = TestRequest(HTTP_IF_MODIFIED_SINCE=formatdate(before, usegmt=True),
        ...                       HTTP_IF_NONE_MATCH='"otheretag"')
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True

    """


def doctest_FileResource_GET_works_without_IETag_adapter():
    """Test backwards compatibility with users of <3.11 that do not provide an ETagAdatper

        >>> getGlobalSiteManager().unregisterAdapter(MyETag)
        True
        >>> factory = FileResourceFactory(testFilePath, nullChecker, 'test.txt')
        >>> request = TestRequest()
        >>> resource = factory(request)
        >>> bool(resource.GET())
        True
        >>> request.response.getHeader('ETag') is None
        True
    """



def test_suite():
    checker = RENormalizing([
        # Python 3 includes module name in exceptions
        (re.compile(r"zope.publisher.interfaces.NotFound"),
         "NotFound"),
    ])

    return unittest.TestSuite((
        doctest.DocTestSuite(
            'zope.browserresource.file',
            setUp=setUp, tearDown=tearDown,
            checker=checker,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        doctest.DocTestSuite(
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        ))
