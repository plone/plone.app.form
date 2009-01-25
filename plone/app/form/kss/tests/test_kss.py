import unittest
from zope.testing import doctest, cleanup
from Products.Five import zcml

import Products.Five
try:
    import kss.core
    import kss.core
    import kss.core.tests
    import plone.app.kss
    HAS_KSS = True
except ImportError:
    HAS_KSS = False

import plone.app.form
import plone.memoize

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE)


def setUp(test):
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('meta.zcml', kss.core)
    zcml.load_config('configure.zcml', kss.core)
    zcml.load_config('configure-unittest.zcml', kss.core.tests)
    zcml.load_config('configure.zcml', plone.app.form)
    zcml.load_config('configure.zcml', plone.memoize)
    zcml.load_config('configure.zcml', plone.app.kss)

def tearDown(test):
    cleanup.cleanUp()

def test_suite():
    if HAS_KSS:
        return unittest.TestSuite([
            doctest.DocFileSuite('kss/formlib_kss.txt',
                                 package='plone.app.form',
                                 setUp=setUp,
                                 tearDown=tearDown,
                                 optionflags=optionflags),
            ])
    return unittest.TestSuite()
