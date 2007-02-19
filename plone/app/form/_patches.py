from Products.Five.formlib import formbase

def apply_patches():

    # Five's base class defines template as a ViewPageTemplateFile.
    # However, the base 'zope.formlib.form.FormBase' has 'template'
    # defined as a NamedTemplate, which is much nicer, and what we
    # want.
    if 'template' in formbase.FiveFormlibMixin.__dict__:
        delattr(formbase.FiveFormlibMixin, 'template')
