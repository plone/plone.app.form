from zope.app.form.browser import CheckBoxWidget
from zope.app.form.browser.widget import renderElement, SimpleInputWidget
from zope.i18nmessageid import MessageFactory
from zope.i18n import translate

_ = MessageFactory('plone')

class CheckBoxPloneWidget(CheckBoxWidget):
    """ Plone specific widget that is going to show the checkbox widget on the left of the label
        in order to do that we remove the title / label / required
    """

    def name( self ):
        return ""

    def label( self ):
        return ""

    def error( self ):
        return ""

    def hint( self ):
        return ""

    def __call__( self ):
        """Render the widget to HTML."""
        value = self._getFormValue()
        html = "<label for='%s'>%s</label>\n" % (self.name , super(CheckBoxWidget,self).label)
        if self.required:
            html += "<span class='fieldRequired' title='%s' > %s </span>" % ( translate(_(u'title_required'),context=self.request), translate(_(u'title_required'),context=self.request))
        if super(CheckBoxWidget, self).hint:
            html += "<div class='formHelp'>%s</div>" % super(CheckBoxWidget, self).hint
        if super(CheckBoxWidget, self).error() != '':
            html += "<div>%s</div>" % super(CheckBoxWidget, self).error
        
        if value == 'on':
            kw = {'checked': 'checked'}
        else:
            kw = {}
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

