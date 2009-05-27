from Products.PloneTestCase import PloneTestCase as ptc
from Products.CMFCore.utils import getToolByName

from zope.publisher.browser import TestRequest
from zope.site.hooks import getSite

from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

ptc.setupPloneSite()


class WYSIWYGWidgetTestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """

    def test_right_macro(self):
        # fixes #8016
        class MyField:
            __name__ = 'the field'
            required = True
            default = u'the value'
            missing_value = None
            title = ""
            description = ""

        # the wysiwyg widget depends on the used editor
        pm = getToolByName(self.portal, 'portal_membership')
        member = pm.getAuthenticatedMember()
        editor = member.getProperty('wysiwyg_editor', '').lower()

        # let's add a custom editor
        # with a fake skin that should be catched
        # to provide a custom macro
        site = getSite()
        class  MyMacros(object):
            def wysiwygEditorBox(self):
                return (('version', '1.6'), ('mode', 'html'))
        class MySkin(object):
            macros = MyMacros()
        site.cool_editor_wysiwyg_support = MySkin()

        # let's change it to `cool_editor`
        member.setMemberProperties({'wysiwyg_editor': 'cool_editor'})

        w = WYSIWYGWidget(MyField(), TestRequest())
        cool_editor = w()

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(WYSIWYGWidgetTestCase))
    return suite
