from zope import interface, schema
from zope.i18n import translate
from zope.formlib import form

from zope.app.form import InputWidget
from zope.app.form.browser.widget import BrowserWidget, SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.i18n import ZopeMessageFactory as _

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile


class ISearch(interface.Interface):
    text = schema.TextLine(title=u'Search Text',
                           description=u'The text to search for',
                           required=False)

    description = schema.TextLine(title=u'Description',
                                  required=True)


class UberSelectionWidget(SimpleInputWidget):
    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __call__(self):
        return self.template()

    def searchButtonLabel(self):
        button_label = _('Search')
        button_label = translate(button_label, context=self.request,
                                 default=button_label)
        return button_label


class SearchForm(form.PageForm):
    form_fields = form.FormFields(ISearch)
    form_fields['text'].custom_widget = UberSelectionWidget

    @form.action("search")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        return repr(data)
