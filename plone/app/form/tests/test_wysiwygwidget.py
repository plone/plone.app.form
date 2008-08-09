from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName

from zope.publisher.browser import TestRequest
from zope.app.component.hooks import getSite

from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    try:
        import plone.app.form
        zcml.load_config('configure.zcml', plone.app.form)
    finally:
        fiveconfigure.debug_mode = False
    ztc.installPackage('plone.app.form')

setup_product()
ptc.setupPloneSite(products=['plone.app.form'])

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

        # the wysiwyg widget depends on the used editor
        pm = getToolByName(self.portal, 'portal_membership')
        member = pm.getAuthenticatedMember()
        editor = member.getProperty('wysiwyg_editor', '').lower()

        # we have kupu by default
        self.assertEquals(editor, 'kupu')

        # so it means the widget should use the macro
        # provided by kupu (default skin with .css includes)
        w = WYSIWYGWidget(MyField(), TestRequest())
        kupu = w()

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

        # the macro used by wysiwygwidget should differ
        self.assertNotEquals(kupu, cool_editor)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(WYSIWYGWidgetTestCase))
    return suite
