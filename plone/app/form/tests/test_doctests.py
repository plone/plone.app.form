# -*- coding: utf-8 -*-
from zope.component import testing
from zope.testing import cleanup
from Zope2.App import zcml

import doctest
import unittest


def setUp(test):
    import five.formlib
    import plone.app.form
    import plone.memoize
    import Products.CMFCore
    import Products.Five

    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', five.formlib)
    zcml.load_config('permissions.zcml', Products.CMFCore)
    zcml.load_config('configure.zcml', plone.app.form)
    zcml.load_config('configure.zcml', plone.memoize)


def tearDown(test):
    cleanup.cleanUp()


def test_suite():
    optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'formlib.txt',
            package='plone.app.form',
            setUp=testing.setUp,
            tearDown=testing.tearDown),
        doctest.DocFileSuite(
            'inline_validation.txt',
            package='plone.app.form',
            setUp=setUp,
            tearDown=tearDown,
            optionflags=optionflags),
    ))
