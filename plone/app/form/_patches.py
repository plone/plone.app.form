
patches = {}

def apply_formlib_update_patch():
    """Formlib (and all of zope3's widget machinery) expects input
    values to already have been converted to unicode objects.  ZPublisher
    (zope2) doesn't take care of this so Five introduced a method in
    its formlib overriding mixin to remedy this.  Let's make sure
    zope.formlib.FormBase has Five's update method.
    """
    
    from zope.formlib import form
    from Products.Five.browser import decode
    patched = patches.get('formlib_formbase_update', None) is not None
    if not patched:
        orig = form.FormBase.update
        patches['formlib_formbase_update'] = (form.FormBase, 'update', 
                                              orig)
        def update(self):
            decode.processInputs(self.request)
            decode.setPageEncoding(self.request)
            orig(self)
            
        form.FormBase.update = update
        return True
    return False

def remove_formlib_update_patch():
    patch = patches.get('formlib_formbase_update', None)
    if patch is not None:
        obj, attr_name, orig = patch
        setattr(obj, attr_name, orig)
        del patches['formlib_formbase_update']
        return True
    return False
