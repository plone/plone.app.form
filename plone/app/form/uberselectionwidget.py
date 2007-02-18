from zope import interface, schema
from zope.component import getMultiAdapter, provideAdapter
from zope.formlib import form
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.form.browser.source import SourceListInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile

from pprint import pprint

class IUberSelect(interface.Interface):
    pass


class UberSelect(schema.Choice):
    interface.implements(IUberSelect)


class MySource(object):
    interface.implements(schema.interfaces.ISource)

    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        return True


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
        return None

    def results(self, name):
        print "results", self.request.form
        if not name+".search":
            return None
        query_fieldname = name+".query"
        if query_fieldname in self.request.form:
            query = self.request.form[query_fieldname]
            if query != '':
                return ('spam', 'spam', 'spam', 'ham', 'eggs')
            else:
                return None
        else:
            return None

provideAdapter(
    QuerySchemaSearchView,
    (MySource, IBrowserRequest)
)


class IUberSelectionDemoForm(interface.Interface):
    text = UberSelect(title=u'Search Text',
                         description=u'The text to search for',
                         required=False,
                         source=MySource())


class UberSelectionWidget(SourceListInputWidget):
    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def _input_value(self):
        tokens = self.request.form.get(self.name)
        for name, queryview in self.queryviews:
                newtokens = self.request.form.get(name+'.selection')
                if newtokens:
                    if tokens:
                        tokens = tokens + newtokens
                    else:
                        tokens = newtokens

        if tokens:
            remove = self.request.form.get(self.name+'.checked')
            if remove and (self.name+'.remove' in self.request):
                tokens = [token
                          for token in tokens
                          if token not in remove
                          ]
            value = []
            for token in tokens:
                try:
                    v = self.terms.getValue(str(token))
                except LookupError:
                    pass # skip invalid tokens (shrug)
                else:
                    value.append(v)
        else:
            if self.name+'.displayed' in self.request:
                value = []
            else:
                value = self.context.missing_value

        if value:
            r = []
            seen = {}
            for s in value:
                if s not in seen:
                    r.append(s)
                    seen[s] = 1
            value = r

        return value

    def queryviews(self):  
        return [
                    (self.name,
                     getMultiAdapter(
                        (self.source, self.request),
                        ISourceQueryView,
                     )
                    )
               ]

    queryviews = property(queryviews)
            
    def __call__(self):
        print "__call__", self.request.form
        value = self._value()
        if value is None:
            value = []
        value = [self.terms.getTerm(x) for x in value]
        print repr(value)
        field = self.context
        results = []
        for name, queryview in self.queryviews:
            qresults = queryview.results(name)
            if qresults is not None:
                for item in qresults:
                    results.append(self.terms.getTerm(item))
        return self.template(field=field, results=results, name=self.name, value=value)


class UberSelectionDemoForm(form.PageForm):
    form_fields = form.FormFields(IUberSelectionDemoForm)

    @form.action("dskljfhsd")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        return repr(data)
