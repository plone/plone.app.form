from zope import interface, schema
from zope.component import getMultiAdapter, provideAdapter
from zope.formlib import form
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.form.browser.source import SourceInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile


class MySource(object):
    interface.implements(schema.interfaces.ISource)

    def __contains__(value):
        """Return whether the value is available in this source
        """
        return False


class MyTerms(object):
    interface.implements(ITerms)

    def __init__(self, source, request):
        pass # We don't actually need the source or the request :)

    def getTerm(self, value):
        title = unicode(value)
        try:
            token = title.encode('base64').strip()
        except binascii.Error:
            raise LookupError(token)
        return schema.vocabulary.SimpleTerm(value, token=token, title=title)

    def getValue(self, token):
        return token.decode('base64')

provideAdapter(
    MyTerms,
    (MySource, IBrowserRequest)
)


class QuerySchemaSearchView(object):
    interface.implements(ISourceQueryView)

    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, name):
        return self.template(name=name)

    def results(self, name):
        # if name in self.request.form:
        #     
        return ('spam', 'spam', 'spam', 'ham', 'eggs')

provideAdapter(
    QuerySchemaSearchView,
    (MySource, IBrowserRequest)
)


class ISearch(interface.Interface):
    text = schema.Choice(title=u'Search Text',
                         description=u'The text to search for',
                         required=False,
                         source=MySource())


class UberSelectionWidget(SimpleInputWidget):
    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __call__(self):
        self._update()
        return self.template()

    def _update(self):
        self.results = ()
        if self.name+".query" in self.request.form:
            factory_name = self.context.results_fetcher
            fetcher = getUtility(IResultFetcherFactory, factory_name)
            self.results = fetcher(self.name)


class SearchForm(form.PageForm):
    form_fields = form.FormFields(ISearch)
    #form_fields['text'].custom_widget = UberSelectionWidget

    @form.action("search")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        return repr(data)
