from zope import interface, schema
from zope.component import getMultiAdapter
from zope.formlib import form

from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile


class ISearch(interface.Interface):
    text = schema.TextLine(title=u'Search Text',
                           description=u'The text to search for',
                           required=False)

    description = schema.TextLine(title=u'Description',
                                  required=True)


class IResultFetcher(interface.Interface):
    """ """

    def __call__(name):
        """ Returns results ((key, value), ...)"""


class UberSelectionWidget(SimpleInputWidget):
    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __call__(self):
        self._update()
        return self.template()

    def _update(self):
        self.results = ()
        if self.name+".query" in self.request.form:
            field = self.context
            fetcher = getMultiAdapter((field.context, self.request), IResultFetcher)
            self.results = fetcher(self.name)


class DummySearch(object):
    interface.implements(IResultFetcher)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, name):
        query = self.request.form[name+'.query']
        print query
        return ('spam', 'spam', 'spam', 'ham', 'eggs')


class SearchForm(form.PageForm):
    form_fields = form.FormFields(ISearch)
    form_fields['text'].custom_widget = UberSelectionWidget

    @form.action("search")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        return repr(data)
