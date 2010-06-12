import unittest
from zope.testing import doctest, cleanup
from Products.Five import zcml

optionflags =  (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def setUp(test):
    import Products.Five
    import Products.CMFCore
    import plone.app.form

    zcml.load_config('configure.zcml', Products.Five)
    try:
        zcml.load_config('permissions.zcml', Products.CMFCore)
    except IOError:
        # BBB CMF 2.2
        pass
    zcml.load_config('configure.zcml', plone.app.form)


def tearDown(test):
    cleanup.cleanUp()


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite('widgets/uberselectionwidget.txt',
                             package='plone.app.form',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=optionflags),
        ])
