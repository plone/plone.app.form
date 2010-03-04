from zope.component import getMultiAdapter
from zope.formlib import form as formlib

from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from Acquisition import aq_inner
from Products.Five.browser.decode import processInputs

class FormlibValidation(PloneKSSView):
    """KSS actions for formlib form inline validation
    """

    @kssaction
    def validate_input(self, formname, fieldname, value=None):
        """Given a form (view) name, a field name and the submitted
        value, validate the given field.
        """
        
        # Abort if there was no value changed. Note that the actual value
        # comes along the submitted form, since a widget may require more than
        # a single form field to validate properly.
        if value is None:
            return
        
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        processInputs(self.request)
        
        # Find the form, the field and the widget

        form = getMultiAdapter((context, request), name=formname)
        form = form.__of__(context)
        
        raw_fieldname = fieldname[len(form.prefix)+1:]
        formlib_field = form.form_fields[raw_fieldname]
 
        widgets = formlib.setUpWidgets((formlib_field,), form.prefix, context, 
            request, form=form, adapters={}, ignore_request=False)
            
        widget = widgets[raw_fieldname]
        
        # Attempt to convert the value - this will trigge validation
        ksscore = self.getCommandSet('core')
        kssplone = self.getCommandSet('plone')
        validate_and_issue_message(ksscore, widget, fieldname, kssplone)
            
def validate_and_issue_message(ksscore, widget, fieldname, kssplone=None):
    """A helper method also used by the inline editing view
    """

    error = None
    try:
        widget.getInputValue()
    except:
        pass
    error = widget.error()

    field_div = ksscore.getHtmlIdSelector('formfield-%s' % fieldname.replace('.', '-'))
    error_box = ksscore.getCssSelector('#formfield-%s div.fieldErrorBox' % fieldname.replace('.', '-'))
    
    if error:
        ksscore.replaceInnerHTML(error_box, error)
        ksscore.addClass(field_div, 'error')
    else:
        ksscore.clearChildNodes(error_box)
        ksscore.removeClass(field_div, 'error')
        if kssplone is not None: 
            kssplone.issuePortalMessage('')

    return bool(error)
