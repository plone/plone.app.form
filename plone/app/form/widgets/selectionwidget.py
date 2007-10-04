from zope.app.form.browser.itemswidgets import DropdownWidget
from zope.component import queryMultiAdapter
from zope.schema.interfaces import ITitledTokenizedTerm


class LanguageDropdownChoiceWidget(DropdownWidget):
    """ A DropdownWidget which renders a localized language selection.
    """

    def __init__(self, field, request):
        """Initialize the widget."""
        super(LanguageDropdownChoiceWidget, self).__init__(field,
            field.vocabulary, request)
        portal_state = queryMultiAdapter((self.context, request),
                                         name=u'plone_portal_state')
        self.languages = portal_state.locale().displayNames.languages

    def textForValue(self, term):
        """Extract a string from the `term`.

        The `term` must be a vocabulary tokenized term.
        """
        if ITitledTokenizedTerm.providedBy(term):
            title = self.languages.get(term.value, term.title)
            if title == term.value:
                title = term.title
            return title
        return term.token
