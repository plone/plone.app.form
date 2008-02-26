from xml.sax.saxutils import unescape

from zope.component import getMultiAdapter
from zope.event import notify

from zope import lifecycleevent
from zope.app.form.interfaces import IDisplayWidget
from zope.formlib import form as formlib

from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.locking.interfaces import ILockable

from plone.app.form.kss.validation import validate_and_issue_message

class FormlibInlineEdit(PloneKSSView):
    """KSS actions for formlib form inline editing
    """

    form_template = ViewPageTemplateFile('inline_edit_wrapper.pt')

    @kssaction
    def begin(self, formname, fieldname, structure='false'):
        """Begin inline editing - find the widget for the given field name
        in the given form (looked up as a view on the context), then hide the
        block with the id '${fieldname}-display' and display an edit form in
        its place. If 'structure' is 'true' (a string), then the inline 
        editable field will eventually permit HTML input to be rendered
        unescaped.
        """
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        
        form = getMultiAdapter((context, request), name=formname)
        form = form.__of__(context)
        
        if fieldname.startswith(form.prefix):
            fieldname = fieldname[len(form.prefix)+1:]
            
        formlib_field = form.form_fields[fieldname]
        widgets = formlib.setUpEditWidgets((formlib_field,), form.prefix, 
            context, request, ignore_request=True)
            
        widget = widgets[fieldname]
        
        display_id = '%s-display' % fieldname
        form_id = '%s-form' % fieldname
        
        ksscore = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        plonecommands = self.getCommandSet('plone')
        
        # lock the context (or issue warning)
        locking = ILockable(context, None)
        if locking:
            if not locking.can_safely_unlock():
                selector = ksscore.getHtmlIdSelector('plone-lock-status')
                zopecommands.refreshViewlet(selector, 'plone.abovecontent', 'plone.lockinfo')
                plonecommands.refreshContentMenu()
                return
            else: # we are locking the content
                locking.lock()
        
        plonecommands.issuePortalMessage('')
        
        # hide the existing display field
        display_selector = ksscore.getHtmlIdSelector(display_id)
        ksscore.addClass(display_selector, 'hiddenStructure')
        
        # show the form
        form_html = self.form_template(widget=widget,
                                       form_id=form_id,
                                       fieldname=fieldname,
                                       structure=structure)

        ksscore.insertHTMLAfter(display_selector, form_html)
        
        # XXX: Focus on the input field?
        
    @kssaction
    def cancel(self, fieldname):
        """Cancel the inline editing taking place for the given field, by
        removing the inline editing form and unhiding the block with id
        '${fieldname}-display'.
        """
        context = aq_inner(self.context)
        
        display_id = '%s-display' % fieldname
        form_id = '%s-form' % fieldname
        
        ksscore = self.getCommandSet('core')
        
        # unlock the context if it was locked before
        locking = ILockable(context, None)
        if locking and locking.can_safely_unlock():
            locking.unlock()

        # show the existing display field
        ksscore.removeClass(ksscore.getHtmlIdSelector(display_id), 'hiddenStructure')
        
        # hide the form
        ksscore.deleteNode(ksscore.getHtmlIdSelector(form_id))
        
    @kssaction
    def save(self, formname, fieldname, structure='false'):
        """Attempt to save the given field in the given form which is being
        inline-edited. If there is a validation error, the error will be
        highlighted. If not, the value will be saved, and the inline editing
        form removed. Before the form is re-displayed, the contents of the
        element with id '${fieldname}-display' will be updated with the new
        field value.
        """
        
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        
        structure = (structure == 'true')
        
        form = getMultiAdapter((context, request), name=formname)
        form = form.__of__(context)
        
        raw_fieldname = fieldname
        if fieldname.startswith(form.prefix):
            raw_fieldname = fieldname[len(form.prefix)+1:]
            full_fieldname = fieldname
        else:
            full_fieldname = "%s.%s" % (form.prefix, raw_fieldname)
            
        formlib_field = form.form_fields[raw_fieldname]
        widgets = formlib.setUpEditWidgets((formlib_field,), form.prefix, 
            context, request, ignore_request=False)
            
        widget = widgets[raw_fieldname]
        
        # validate and issue a message if there's an error
        
        ksscore = self.getCommandSet('core')
        error = validate_and_issue_message(ksscore, widget, full_fieldname)

        if not error:
        
            field_value = request.form.get('%s.%s' % (form.prefix, raw_fieldname))
            data = { raw_fieldname : field_value }
        
            # update value
            changed = formlib.applyChanges(context, (formlib_field,), data)
            if changed:
                
                # send modified events if something actually changed
                field = widget.context
                adapter = field.interface(context)
                
                descriptor = lifecycleevent.Attributes(field.interface, raw_fieldname)
                notify(lifecycleevent.ObjectModifiedEvent(context, descriptor))
                
                # update the rendered value
                display_widget = getMultiAdapter((formlib_field.field, request), IDisplayWidget)
                display_widget.setRenderedValue(field.get(adapter))
                output = display_widget()
                
                if structure:
                    output = unescape(output)
                
                display_id = '%s-display' % fieldname
                ksscore.replaceInnerHTML(ksscore.getHtmlIdSelector(display_id), output)
        
            # unlock and remove the field
            self.cancel(fieldname)