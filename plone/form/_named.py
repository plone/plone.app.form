import os
import new
import AccessControl
import Acquisition
from zope import interface
from zope.formlib import namedtemplate
from Products.Five.browser import metaconfigure
from Products.PageTemplates import ZopePageTemplate

def proper_name(filename):
    basepath, ext = os.path.splitext(filename)
    name = basepath
    if ext and ext.lower() not in ('.pt', '.zpt'):
        name += ext
    
    return os.path.basename(name)

class NamedTemplateAdapter(Acquisition.Explicit):
    interface.implements(namedtemplate.INamedTemplate)

    def __init__(self, context):
        self.context = context
        self._template = [self.default_template]
        
    def __call__(self, *args, **kwargs):
        view = self.context
        cleanup = []
        if isinstance(view, metaconfigure.ViewMixinForTemplates):
            index = getattr(view, 'index', None)
            if index is not None:
                name = proper_name(index.filename)
                template = view.context.portal_url.getPortalObject().restrictedTraverse(name)
                template = template.aq_base.__of__(view.context)

                if isinstance(template, ZopePageTemplate.ZopePageTemplate):
                    def _pt_context(view=view, 
                                    template=template, 
                                    orig_pt_getContext=template.pt_getContext):
                        cdict = orig_pt_getContext()
                        cdict['view'] = view
                        return cdict
                    template.pt_getContext = _pt_context
                    cleanup.append('pt_getContext')
        else:
            template = self.default_template[0].__of__(view)
            def context_builder(self, view=view):
                cdict = self.pt_getContext()
                cdict['view'] = view
                return cdict
            template.pt_getContext = context_builder

        result = template(*args, **kwargs)
        for x in cleanup:
            template.__delattr__(x)
        return result

def named_template_adapter(template):
    new_class = new.classobj('GeneratedClass', 
                             (NamedTemplateAdapter,),
                             {})
    new_class.default_template = [template]
    
    AccessControl.allow_class(new_class)
    return new_class
