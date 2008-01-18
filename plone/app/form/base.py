from zope.interface import implements
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.formlib import form

import zope.event

from zope.app.event.objectevent import ObjectModifiedEvent

from Products.Five.formlib import formbase
from Products.CMFPlone import PloneMessageFactory as _

from plone.app.form.interfaces import IPlonePageForm
from plone.app.form.interfaces import IEditForm
from plone.app.form.validators import null_validator
from plone.app.form.events import EditBegunEvent, EditCancelledEvent, EditSavedEvent

class AddForm(formbase.AddForm):
    """An add form with standard Save and Cancel buttons
    """
    
    implements(IPlonePageForm)
        
    @form.action(_("Save"), condition=form.haveInputWidgets)
    def handle_save_action(self, action, data):
        self.createAndAdd(data)
    
    @form.action(_("Cancel"), validator=null_validator)
    def handle_cancel_action(self, action, data):
        self.request.response.redirect(self.nextURL())


class EditForm(formbase.EditForm):
    """An edit form with standard Save and Cancel buttons
    """
    
    implements(IPlonePageForm, IEditForm)
    
    def update(self):
        zope.event.notify(EditBegunEvent(self.context))
        super(EditForm, self).update()
        
    def render(self):
        # If the object is locked, don't show any widgets
        lock_info = queryMultiAdapter((self.context, self.request), name="plone_lock_info")
        if lock_info is not None and lock_info.is_locked_for_current_user():
            self.widgets = form.Widgets([], prefix=self.prefix)
            self.form_name = None # hide border
        return super(EditForm, self).render()
    
    @form.action(_("Save"), condition=form.haveInputWidgets)
    def handle_save_action(self, action, data):
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(ObjectModifiedEvent(self.context))
            zope.event.notify(EditSavedEvent(self.context))
            self.status = "Changes saved"
        else:
            zope.event.notify(EditCancelledEvent(self.context))
            self.status = "No changes"
            
        url = getMultiAdapter((self.context, self.request), name='absolute_url')()
        self.request.response.redirect(url)
            
    @form.action(_("Cancel"), validator=null_validator)
    def handle_cancel_action(self, action, data):
        zope.event.notify(EditCancelledEvent(self.context))
        url = getMultiAdapter((self.context, self.request), name='absolute_url')()
        self.request.response.redirect(url)
