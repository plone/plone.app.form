from zope import interface, schema
from zope.formlib import form
from zope.app.form import InputWidget
from zope.app.form.browser.widget import BrowserWidget, SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile


class ISearch(interface.Interface):
    text = schema.TextLine(title=u'Search Text',
                           description=u'The text to search for',
                           required=False)

    description = schema.TextLine(title=u'Description',
                                  required=False)


class UberSelectionWidget(SimpleInputWidget):
    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __call__(self):
        return self.template()


class SearchForm(form.PageForm):
    form_fields = form.FormFields(ISearch)
    form_fields['text'].custom_widget = UberSelectionWidget

    @form.action("search")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        kwargs = {}
        if data['text']:
            kwargs['SearchableText'] = data['text']
        if data['description']:
            kwargs['description'] = data['description']

        self.search_results = catalog(**kwargs)
        self.search_results_count = len(self.search_results)
        return repr(self.search_results)
