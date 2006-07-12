import new
import AccessControl
import Acquisition
from zope import interface
from zope.formlib import namedtemplate

class NamedTemplateAdapter(Acquisition.Explicit):
    interface.implements(namedtemplate.INamedTemplate)

    def __init__(self, context):
        self.context = context
        self._template = [self.default_template]
        
    def __call__(self):
        template = self.default_template[0].__of__(self.context)
        return template()

def named_template_adapter(template):
    new_class = new.classobj('GeneratedClass', 
                             (NamedTemplateAdapter,),
                             {})
    new_class.default_template = [template]
    
    AccessControl.allow_class(new_class)
    return new_class
