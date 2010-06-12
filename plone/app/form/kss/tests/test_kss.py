import doctest
import unittest

from zope.testing import cleanup

# BBB Zope 2.12
try:
    from Zope2.App import zcml
except ImportError:
    from Products.Five import zcml

try:
    import kss.core
    import kss.core.tests
    import plone.app.kss
    HAS_KSS = True
except ImportError:
    HAS_KSS = False


def setUp(test):
    import five.formlib
    import plone.app.form
    import plone.memoize
    import Products.CMFCore
    import Products.Five

    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', five.formlib)
    zcml.load_config('meta.zcml', kss.core)
    zcml.load_config('configure.zcml', kss.core)
    zcml.load_config('configure-unittest.zcml', kss.core.tests)
    try:
        zcml.load_config('permissions.zcml', Products.CMFCore)
    except IOError:
        # BBB CMF 2.2
        pass
    zcml.load_config('configure.zcml', plone.app.form)
    zcml.load_config('configure.zcml', plone.memoize)
    zcml.load_config('configure.zcml', plone.app.kss)

def tearDown(test):
    cleanup.cleanUp()

def test_suite():
    if HAS_KSS:
        optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
        return unittest.TestSuite([
            doctest.DocFileSuite('kss/formlib_kss.txt',
                                 package='plone.app.form',
                                 setUp=setUp,
                                 tearDown=tearDown,
                                 optionflags=optionflags),
            ])
    return unittest.TestSuite()
