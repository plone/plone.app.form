# -*- coding: utf-8 -*-
from zope.formlib.boolwidgets import CheckBoxWidget as BaseWidget
from zope.formlib.widget import renderElement
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone')


class CheckBoxWidget(BaseWidget):
    """ Plone specific widget that is going to show the checkbox widget on the left of the label
        in order to do that we remove the title / label / required
    """

    def __init__(self, context, request):
        BaseWidget.__init__(self, context, request)
        self.required = False
        self.__required = context.required
        self.label = ""
        self.hint = ""

    disabled = False

    def __call__(self):
        """Render the widget to HTML."""
        value = self._getFormValue()
        html = u"<label for='{0}'>{1}".format(
            self.name,
            translate(self.context.title, context=self.request)
        )
        if self.__required:
            # Use the numeric character reference here instead of &nbsp; to make
            # our xml-parsing tests happier.
            html += u" <span class='required' title='{0}'>&#160;</span>".format(
                translate(_(u'title_required', default='Required'), context=self.request)
            )
        if self.context.description:
            html += u" <span class='formHelp'>{0}</span>".format(
                translate(self.context.description, context=self.request)
            )
        html += u"</label>\n"

        if value == 'on':
            kw = {'checked': 'checked'}
        else:
            kw = {}
        if self.disabled:
            kw['disabled'] = 'disabled'
        return u'{0}  {1} {2}'.format(
            renderElement(self.tag,
                          type='hidden',
                          name=self.name + ".used",
                          id=self.name + ".used",
                          value=""
                          ),
            renderElement(self.tag,
                          type=self.type,
                          name=self.name,
                          id=self.name,
                          cssClass=self.cssClass,
                          extra=self.extra,
                          value="on",
                          **kw),
            html
        )


class DisabledCheckBoxWidget(CheckBoxWidget):
    """Simple variation of the CheckBoxWidget which renders itself disabled.
    """

    disabled = True
