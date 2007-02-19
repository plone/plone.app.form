from zope import interface, schema
from Products.Five.formlib import formbase
from zope.formlib import form

class ITestSchema(interface.Interface):
    foo = schema.TextLine(title=u'Foo',
                          description=u'Some Random Description')
    bar = schema.Bool(title=u'Bar')

class TestForm(formbase.FormBase):
    """foo
    """
    
    form_fields = form.FormFields(ITestSchema)
    actions = ()
