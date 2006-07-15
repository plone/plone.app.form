import os
import new
import AccessControl
import Acquisition
from zope import interface
from zope.formlib import namedtemplate
from Products.Five.browser import metaconfigure
from Products.PageTemplates import ZopePageTemplate

def proper_name(filename):
    """Get the base name of a possibly full path and if it ends with
    .pt or .zpt, chop it off.
    """
    
    basepath, ext = os.path.splitext(filename)
    name = basepath
    if ext and ext.lower() not in ('.pt', '.zpt'):
        name += ext
    
    return os.path.basename(name)

class NamedTemplateAdapter(Acquisition.Explicit):
    """A named template adapter implementation that has the ability
    to lookup the template portion from regular traversal (intended for
    being able to customize the template portion of a view component
    in the traditional portal_skins style).
    """
    
    interface.implements(namedtemplate.INamedTemplate)

    def __init__(self, context):
        self.context = context
        self._template = [self.default_template]
        
    def __call__(self, *args, **kwargs):
        view = self.context
        cleanup = []
        
        # basically this means we only do customized template lookups
        # for views defined with <browser:page template='foo'> 
        if isinstance(view, metaconfigure.ViewMixinForTemplates):
            index = getattr(view, 'index', None)
            if index is not None:
                name = proper_name(index.filename)
                try:
                    template = view.context.portal_url.getPortalObject().restrictedTraverse(name)
                except AttributeError:
                    # ok, we couldn't find a portal_skins defined item
                    # so we fall back to the defined page template
                    template = index
                else:
                    template = template.aq_base.__of__(view.context)
    
                    # here we dynamically monkey a page template instance
                    # so that we can insert the view variable into
                    # the template's global namespace... evil, but its
                    # what we do until we find a better way
                    if isinstance(template, ZopePageTemplate.ZopePageTemplate):
                        def _pt_context(view=view, 
                                        template=template, 
                                        orig_pt_getContext=template.pt_getContext):
                            cdict = orig_pt_getContext()
                            cdict['view'] = view
                            return cdict
                        template.pt_getContext = _pt_context
                        cleanup.append('pt_getContext')

        result = template(*args, **kwargs)
        for x in cleanup:
            template.__delattr__(x)
        return result

def named_template_adapter(template):
    """Return a new named template adapter which defaults the to given
    template.
    """
    
    new_class = new.classobj('GeneratedClass', 
                             (NamedTemplateAdapter,),
                             {})
    new_class.default_template = [template]
    
    AccessControl.allow_class(new_class)
    return new_class
