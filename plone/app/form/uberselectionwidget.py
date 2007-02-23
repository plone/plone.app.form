from zope import interface, schema
from zope.component import getMultiAdapter, provideAdapter
from zope.formlib import form
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from Products.CMFCore import utils as cmfutils
from Products.Five.browser import pagetemplatefile

from pprint import pprint


class MySource(object):
    interface.implements(schema.interfaces.ISource)
    interface.classProvides(schema.interfaces.IContextSourceBinder)

    def __init__(self, context):
        self.context = context

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
        return schema.vocabulary.SimpleTerm(value, token=value, title=title)

    def getValue(self, token):
        return token


class QueryMySourceView(object):
    interface.implements(ISourceQueryView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def results(self, name):
        if not name+".search" in self.request.form:
            return None
        query_fieldname = name+".query"
        if query_fieldname in self.request.form:
            query = self.request.form[query_fieldname]
            if query != '':
                return tuple(('spam%i' % (i+1)) for i in range(200))
            else:
                return None
        else:
            return None


class UberSelectionWidget(SimpleInputWidget):
    _error = None

    template = ViewPageTemplateFile('uberselectionwidget.pt')

    def __init__(self, field, request):
        SimpleInputWidget.__init__(self, field, request)
        self.source = field.source
        self.terms = getMultiAdapter((field.source, self.request), ITerms)
        self.queryview = getMultiAdapter((field.source, self.request), ISourceQueryView)

    def _value(self):
        if self._renderedValueSet():
            value = self._data
        else:
            token = self.request.form.get(self.name)

            if token is not None:
                if not isinstance(token, basestring):
                    token = token[-1]
                try:
                    value = self.terms.getValue(str(token))
                except LookupError:
                    value = self.context.missing_value
            else:
                value = self.context.missing_value

        return value

    def _getRenderValue(self):
        value = self._value()
        if value is not None:
            value = self.terms.getTerm(value)
        return value

    def hidden(self):
        value = self._value()
        if value == self.context.missing_value:
            return '' # Nothing to hide ;)

        try:
            term = self.terms.getTerm(value)
        except LookupError:
            # A value was set, but it's not valid.  Treat
            # it as if it was missing and return nothing.
            return ''

        return '<input type="hidden" name="%s" value="%s" />' % (self.name, term.token)

    def error(self):
        if self._error:
            return getMultiAdapter((self._error, self.request),
                                   IWidgetInputErrorView).snippet()
        return ""

    def __call__(self):
        value = self._getRenderValue()
        field = self.context
        results = []
        results_truncated = False
        qresults = self.queryview.results(self.name)
        if qresults is not None:
            for index, item in enumerate(qresults):
                if index >= 20:
                    results_truncated = True
                    break
                results.append(self.terms.getTerm(item))
        return self.template(field=field,
                             results=results,
                             results_truncated=results_truncated,
                             name=self.name,
                             value=value)

    def getInputValue(self):
        token = self.request.get(self.name)

        field = self.context

        if token is None:
            if field.required:
                raise zope.app.form.interfaces.MissingInputError(
                    field.__name__, self.label,
                    )
            return field.missing_value

        try:
            value = self.terms.getValue(str(token))
        except LookupError:
            err = zope.schema.interfaces.ValidationError(
                "Invalid value id", token)
            raise WidgetInputError(field.__name__, self.label, err)

        # Remaining code copied from SimpleInputWidget

        # value must be valid per the field constraints
        try:
            field.validate(value)
        except ValidationError, err:
            self._error = WidgetInputError(field.__name__, self.label, err)
            raise self._error

        return value

    def hasInput(self):
        if self.name in self.request or self.name+'.displayed' in self.request:
            return True

        token = self.request.form.get(self.name)
        if token is not None:
            return True

        return False

class UberMultiSelectionWidget(UberSelectionWidget):
    template = ViewPageTemplateFile('ubermultiselectionwidget.pt')

    def _value(self):
        if self._renderedValueSet():
            value = self._data
        else:
            tokens = self.request.form.get(self.name)

            if tokens is not None:
                value = []
                for token in tokens:
                    try:
                        v = self.terms.getValue(str(token))
                    except LookupError:
                        pass # skip invalid values
                    else:
                        value.append(v)
            else:
                if self.name+'.displayed' in self.request:
                    value = []
                else:
                    value = self.context.missing_value

        return value

    def _getRenderValue(self):
        value = self._value()
        if value is not None:
            value = [self.terms.getTerm(x) for x in value]
        return value


class IUberSelectionDemoForm(interface.Interface):
    selection = schema.Choice(title=u'Single select',
                         description=u'Select just one item',
                         required=False,
                         source=MySource)

    multiselection = schema.Choice(title=u'Multi select',
                         description=u'Select multiple items',
                         required=False,
                         source=MySource)


class UberSelectionDemoForm(form.PageForm):
    form_fields = form.FormFields(IUberSelectionDemoForm)
    form_fields['selection'].custom_widget = UberSelectionWidget
    form_fields['multiselection'].custom_widget = UberMultiSelectionWidget

    @form.action("dskljfhsd")
    def action_search(self, action, data):
        catalog = cmfutils.getToolByName(self.context, 'portal_catalog')

        return repr(data)
