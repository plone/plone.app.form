# -*- coding: utf-8 -*-
from zope.testing import cleanup
from Zope2.App import zcml

import doctest
import unittest


def setUp(test):
    import Products.Five
    import Products.CMFCore
    import plone.app.form

    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('permissions.zcml', Products.CMFCore)
    zcml.load_config('configure.zcml', plone.app.form)


def tearDown(test):
    cleanup.cleanUp()


def test_suite():
    optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    return unittest.TestSuite([
        doctest.DocFileSuite('widgets/uberselectionwidget.txt',
                             package='plone.app.form',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=optionflags),
        doctest.DocFileSuite('widgets/checkboxwidget.txt',
                             package='plone.app.form',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=optionflags),
    ])
