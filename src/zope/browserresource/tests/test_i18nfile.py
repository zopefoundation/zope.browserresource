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
"""I18n File-Resource Tests
"""
import os
from unittest import TestCase

from zope.component import adapter
from zope.component import provideAdapter
from zope.component import provideUtility
from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import IUserPreferredCharsets
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.negotiator import negotiator
from zope.interface import implementer
from zope.publisher.browser import BrowserLanguages
from zope.publisher.browser import TestRequest
from zope.publisher.http import HTTPCharsets
from zope.publisher.http import IHTTPRequest
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.testing import cleanup

import zope.browserresource.tests as p
from zope.browserresource.file import File
from zope.browserresource.i18nfile import I18nFileResource
from zope.browserresource.i18nfile import I18nFileResourceFactory
from zope.browserresource.interfaces import IETag
from zope.browserresource.interfaces import IFileResource


test_directory = os.path.dirname(p.__file__)


class AbstractTestII18nAwareMixin:

    def setUp(self):
        super().setUp()
        self.object = self._createObject()
        self.object.setDefaultLanguage('fr')

    def _createObject(self):
        # Should create an object that has lt, en and fr as available
        # languages
        raise NotImplementedError()

    def testGetDefaultLanguage(self):
        self.assertEqual(self.object.getDefaultLanguage(), 'fr')

    def testSetDefaultLanguage(self):
        self.object.setDefaultLanguage('lt')
        self.assertEqual(self.object.getDefaultLanguage(), 'lt')

    def testGetAvailableLanguages(self):
        self.assertEqual(
            sorted(self.object.getAvailableLanguages()),
            ['en', 'fr', 'lt'])


@adapter(IFileResource, IBrowserRequest)
@implementer(IETag)
class MyETag:

    def __init__(self, context, request):
        pass

    def __call__(self, mtime, content):
        return 'myetag'


class Test(AbstractTestII18nAwareMixin, cleanup.CleanUp, TestCase):

    def setUp(self):
        super().setUp()
        provideAdapter(HTTPCharsets, (IHTTPRequest,), IUserPreferredCharsets)
        provideAdapter(BrowserLanguages, (IHTTPRequest,),
                       IUserPreferredLanguages)
        # Setup the negotiator utility
        provideUtility(negotiator, INegotiator)
        provideAdapter(MyETag)

    def _createObject(self):
        obj = I18nFileResource({'en': None, 'lt': None, 'fr': None},
                               TestRequest(), 'fr')
        return obj

    def test_setDefaultLanguage(self):
        ob = self._createObject()
        self.assertRaises(ValueError, ob.setDefaultLanguage, 'ru')

    def _createDict(self, filename1='test.html', filename2='test2.html'):
        path1 = os.path.join(test_directory, 'testfiles', filename1)
        path2 = os.path.join(test_directory, 'testfiles', filename2)
        return {
            'en': File(path1, filename1),
            'fr': File(path2, filename2)
        }

    def testNoTraversal(self):

        resource = I18nFileResourceFactory(
            self._createDict(), 'en')(TestRequest())

        self.assertRaises(NotFound,
                          resource.publishTraverse,
                          resource.request,
                          '_testData')

    def testFileGET(self):

        # case 1: no language preference, should get en
        path = os.path.join(test_directory, 'testfiles', 'test.txt')

        resource = I18nFileResourceFactory(
            self._createDict('test.txt'), 'en')(TestRequest())

        with open(path, 'rb') as f:
            self.assertEqual(resource.GET(), f.read())

        response = resource.request.response
        self.assertEqual(response.getHeader('Content-Type'), 'text/plain')

        # case 2: prefer lt, have only en and fr, should get en
        resource = I18nFileResourceFactory(
            self._createDict('test.txt'), 'en')(
            TestRequest(HTTP_ACCEPT_LANGUAGE='lt'))

        with open(path, 'rb') as f:
            self.assertEqual(resource.GET(), f.read())

        response = resource.request.response
        self.assertEqual(response.getHeader('Content-Type'), 'text/plain')

        # case 3: prefer fr, have it, should get fr
        path = os.path.join(test_directory, 'testfiles', 'test2.html')
        resource = I18nFileResourceFactory(
            self._createDict('test.html', 'test2.html'), 'en')(
            TestRequest(HTTP_ACCEPT_LANGUAGE='fr'))

        with open(path, 'rb') as f:
            self.assertEqual(resource.GET(), f.read())

        response = resource.request.response
        self.assertEqual(response.getHeader('Content-Type'), 'text/html')

    def testFileHEAD(self):

        # case 1: no language preference, should get en
        resource = I18nFileResourceFactory(
            self._createDict('test.txt'), 'en')(TestRequest())

        self.assertEqual(resource.HEAD(), b'')

        response = resource.request.response
        self.assertEqual(response.getHeader('Content-Type'), 'text/plain')

        # case 2: prefer lt, have only en and fr, should get en
        resource = I18nFileResourceFactory(
            self._createDict('test.txt'), 'en')(
            TestRequest(HTTP_ACCEPT_LANGUAGE='lt'))

        self.assertEqual(resource.HEAD(), b'')

        response = resource.request.response
        self.assertEqual(response.getHeader('Content-Type'), 'text/plain')

        # case 3: prefer fr, have it, should get fr
        resource = I18nFileResourceFactory(
            self._createDict('test.html', 'test2.html'), 'en')(
            TestRequest(HTTP_ACCEPT_LANGUAGE='fr'))

        self.assertEqual(resource.HEAD(), b'')

        response = resource.request.response
        self.assertEqual(response.getHeader('Content-Type'), 'text/html')
