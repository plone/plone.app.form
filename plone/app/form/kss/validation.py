from zope.component import getMultiAdapter
from zope.formlib import form as formlib

from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from Acquisition import aq_inner

class FormlibValidation(PloneKSSView):
    """KSS actions for formlib form inline validation
    """

    @kssaction
    def validate_input(self, formname, fieldname, value=None):
        """Given a form (view) name, a field name and the submitted
        value, validate the given field.
        """
        
        # Abort if this was not bound properly, e.g. it's a submit button
        # in the middle of the form
        if value is None:
            return
        
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        
        # Fake input in the request
        
        request.form[fieldname] = value
        
        # Find the form, the field and the widget

        form = getMultiAdapter((context, request), name=formname)
        form = form.__of__(context)
        
        raw_fieldname = fieldname[len(form.prefix)+1:]
        formlib_field = form.form_fields[raw_fieldname]
 
        widgets = formlib.setUpWidgets((formlib_field,), form.prefix, context, 
            request, form=form, adapters={}, ignore_request=True)
            
        widget = widgets[raw_fieldname]
        
        # Attempt to convert the value - this will trigge validation
        ksscore = self.getCommandSet('core')
        validate_and_issue_message(ksscore, widget, fieldname)
            
def validate_and_issue_message(ksscore, widget, fieldname):
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
        
    return bool(error)