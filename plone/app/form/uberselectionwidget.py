from zope import interface, schema
from zope.component import getMultiAdapter
from zope.formlib import form

from zope.app.form.browser.source import SourceListInputWidget
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

    def __call__(query):
        """ Returns results ((key, value), ...)"""


class UberSelectionWidget(SourceListInputWidget):
    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __call__(self):
        return self.template()




class DummySearch(object):
    interface.implements(IResultFetcher)

    def __init__(self, context, field):
        self.context = context
        self.field = field

    def __call__(self, query):
        print query
        return ()


class SearchForm(form.PageForm):
    form_fields = form.FormFields(ISearch)
    form_fields['text'].custom_widget = UberSelectionWidget

    @form.action("search")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        return repr(data)
