from base import FormFunctionalTestCase

import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import ZopeDocTestSuite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def test_suite():
    return unittest.TestSuite(
        [ZopeDocTestSuite(module,
                          test_class=FormFunctionalTestCase,
                          optionflags=optionflags)
          for module in ('plone.app.form.uberselectionwidget',)]
        )
