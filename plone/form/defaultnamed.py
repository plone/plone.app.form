import Acquisition
from zope import interface
from zope.formlib import namedtemplate
from Products.Five.browser import pagetemplatefile

default_template = pagetemplatefile.ViewPageTemplateFile('pageform.pt')

class FiveNamedTemplateAdapter(Acquisition.Explicit):
    interface.implements(namedtemplate.INamedTemplate)
        
    def __init__(self, context):
        # since context will be the view, we actually want the view's context
        self.context = context
    
    def __call__(self):
        template = default_template.__of__(self.context)
        return template()

import AccessControl
AccessControl.allow_class(FiveNamedTemplateAdapter)
