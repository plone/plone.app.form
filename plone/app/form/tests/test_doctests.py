import doctest
import unittest

from zope.component import testing


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('formlib.txt',
                             package='plone.app.form',
                             setUp=testing.setUp,
                             tearDown=testing.tearDown),
        ))
