import unittest
import Products.Five
import plone.app.form
from zope.testing import doctest, cleanup
from Products.Five import zcml

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)


def setUp(test):
    zcml.load_config('configure.zcml', Products.Five)
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
