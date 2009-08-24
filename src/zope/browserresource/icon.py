##############################################################################
#
# Copyright (c) 2002 Zope Corporation and Contributors.
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
"""Icon support

$Id$
"""
from zope.traversing.namespace import getResource

class IconView(object):

    def __init__(self, context, request, rname, alt, width, height):
        self.context = context
        self.request = request
        self.rname = rname
        self.alt = alt
        self.width = width
        self.height = height

    def __call__(self):
        return ('<img src="%s" alt="%s" width="%s" height="%s" border="0" />'
                % (self.url(), self.alt, self.width, self.height))

    def url(self):
        # The context is important here, since it becomes the parent of the
        # icon, which is needed to generate the absolute URL.
        resource = getResource(self.context, self.rname, self.request)
        return resource()

class IconViewFactory(object):

    def __init__(self, rname, alt, width, height):
        self.rname = rname
        self.alt = alt
        self.width = width
        self.height = height

    def __call__(self, context, request):
        return IconView(context, request, self.rname, self.alt,
                       self.width, self.height)
