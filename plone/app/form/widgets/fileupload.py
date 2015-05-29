##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Custom formlib fileupload widget. """


from plone.app.form.widgets.interfaces import IFileUpload
from zope.app.form.browser import FileWidget
from zope.app.form.interfaces import ConversionError
from zope.app.form.interfaces import IInputWidget
from zope.interface import implementsOnly
from zope.component import adapts
from zope.publisher.interfaces.browser import IBrowserRequest


class FileUploadWidget(FileWidget):

    implementsOnly(IInputWidget)
    adapts(IFileUpload, IBrowserRequest)

    def _toFieldValue(self, input):
        if not input:
            return self.context.missing_value
        try:
            filename = input.filename.split('\\')[-1] # for IE
            input.filename = filename.strip().replace(' ','_')
        except AttributeError, e:
            raise ConversionError(zope_('Form input is not a file object'), e)
        return input

    def hasInput(self):
        return ((self.required and self.name+".used" in self.request.form) or
                self.request.form.get(self.name))


