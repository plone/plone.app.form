from zope.interface import implements
from zope.component import getMultiAdapter
from zope.formlib import form

import zope.event
import zope.lifecycleevent

from Products.CMFPlone import PloneMessageFactory as _

from plone.app.form.interfaces import IPlonePageForm
from plone.app.form.validators import null_validator

class AddForm(form.AddForm):
    """An add form with standard Save and Cancel buttons
    """
    
    implements(IPlonePageForm)
        
    @form.action(_("Save"), condition=form.haveInputWidgets)
    def handle_save_action(self, action, data):
        self.createAndAdd(data)
    
    @form.action(_("Cancel"), validator=null_validator)
    def handle_cancel_action(self, action, data):
        self.request.response.redirect(self.nextURL())


class EditForm(form.EditForm):
    """An edit form with standard Save and Cancel buttons
    """
    
    implements(IPlonePageForm)
    
    @form.action(_("Save"), condition=form.haveInputWidgets)
    def handle_save_action(self, action, data):
        
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            self.status = "Changes saved"
        else:
            self.status = "No changes"
            
        url = getMultiAdapter((self.context, self.request), name='absolute_url')()
        self.request.response.redirect(url)
            
    @form.action(_("Cancel"), validator=null_validator)
    def handle_cancel_action(self, action, data):
        url = getMultiAdapter((self.context, self.request), name='absolute_url')()
        self.request.response.redirect(url)