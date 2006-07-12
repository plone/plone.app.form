from Products.Five.browser import pagetemplatefile

from plone.form._named import named_template_adapter

default_named_template_adapter = named_template_adapter(pagetemplatefile.\
    ViewPageTemplateFile('pageform.pt'))
