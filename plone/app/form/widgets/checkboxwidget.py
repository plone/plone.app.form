from zope.app.form.browser.widget import renderElement
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate
from zope.app.form.browser import CheckBoxWidget as BaseWidget

_ = MessageFactory('plone')

class CheckBoxWidget(BaseWidget):
    """ Plone specific widget that is going to show the checkbox widget on the left of the label
        in order to do that we remove the title / label / required
    """

    def __init__(self, context, request):
        BaseWidget.__init__(self, context, request)
        self.required = self.__required = False
        self.__name = self.name
        self.name = ""

    label = property(lambda self: "")

    hint = property(lambda self: "")

    disabled = False

    def error(self):
        return ""

    def __call__( self ):
        """Render the widget to HTML."""
        value = self._getFormValue()
        html = "<label for='%s'>%s</label>\n" % (self.name , translate(super(BaseWidget,self).label, context=self.request))
        if self.__required:
            html += "<span class='fieldRequired' title='%s'>%s</span>" % (translate(_(u'title_required', default='Required'), context=self.request), translate(_(u'label_required', default='(Required)'), context=self.request))
        if super(BaseWidget, self).hint:
            html += "<div class='formHelp'>%s</div>" % translate(super(BaseWidget, self).hint, context=self.request)
        if super(BaseWidget, self).error() != '':
            html += "<div>%s</div>" % translate(super(BaseWidget, self).error(), context=self.request)
        
        if value == 'on':
            kw = {'checked': 'checked'}
        else:
            kw = {}
        if self.disabled:
            kw['disabled'] = 'disabled'
        return "%s  %s %s" % (
            renderElement(self.tag,
                          type='hidden',
                          name=self.name+".used",
                          id=self.name+".used",
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
