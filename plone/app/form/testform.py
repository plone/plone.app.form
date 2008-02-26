from zope.interface import Interface
from zope import schema

from zope.formlib import form
from Products.Five.formlib import formbase

from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.form import base

class ITestForm(Interface):
    
    required_test = schema.TextLine(
                        title=u"Required",
                        required=True)
    
    int_field = schema.Int(
                        title=u"Int field",
                        required=False
                      )
                
class TestForm(formbase.PageForm):
    form_fields = form.FormFields(ITestForm)
    label = u"Test form"
    
    @form.action("OK")
    def action_ok(self, action, data):
        """Send the email to the site administrator and redirect to the
        front page, showing a status message to say the message was received.
        """
        context = aq_inner(self.context)
        status = IStatusMessage(self.request)
        status.addStatusMessage("You sent " + str(data), type="info")
        self.request.response.redirect(context.absolute_url())
        return ''
        
class ITestEditForm(Interface):
    """Schema used for an edit form
    """
        
    title = schema.TextLine(
                        title=u"Title",
                        required=True)
                        
    description = schema.Text(
                        title=u"Description",
                        required=False)
                        
    text = schema.Text(
                        title=u"Title",
                        required=False)
                        
# wire it up
from zope.component import provideAdapter
from Products.ATContentTypes.interface import IATDocument

class TestEditAdapter(object):
    
    def __init__(self, context):
        self.context = context
        
    def _get_title(self):
        return self.context.Title()
    def _set_title(self, value):
        self.context.setTitle(value)
    title = property(_get_title, _set_title)
    
    def _get_description(self):
        return self.context.Description()
    def _set_description(self, value):
        self.context.setDescription(value)
    description = property(_get_description, _set_description)
    
    def _get_text(self):
        return self.context.getRawText()
    def _set_text(self, value):
        self.context.setText(value)
    text = property(_get_text, _set_text)
    
provideAdapter(factory=TestEditAdapter, adapts=(IATDocument,), provides=ITestEditForm)
    
class TestEditForm(base.EditForm):
    """Test edit form
    """
    
    form_fields = form.FormFields(ITestEditForm)
    
    label = "Test edit"
    form_name = "Test edit"