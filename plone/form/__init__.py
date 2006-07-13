from Products.Five.browser import pagetemplatefile
from plone.form._named import named_template_adapter

__all__ = ('named_template_adapter', 'default_named_template')

_template = pagetemplatefile.ViewPageTemplateFile('pageform.pt')
default_named_template_adapter = named_template_adapter(_template)
