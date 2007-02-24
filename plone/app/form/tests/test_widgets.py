import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import FunctionalDocFileSuite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

# def test_suite():
#     return unittest.TestSuite((
#         FunctionalDocFileSuite('../uberselectionwidget.txt',
#                                optionflags=optionflags),
#         ))
