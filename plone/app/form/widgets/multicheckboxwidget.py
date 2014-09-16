# -*- coding: utf-8 -*-
from zope.formlib.itemswidgets import MultiCheckBoxWidget as BaseWidget
from zope.formlib.widget import renderElement


class MultiCheckBoxWidget(BaseWidget):
    """Provide a list of checkboxes that provide the choice for the list,
       with a <label> for accessibility"""

    orientation = "vertical"

    _joinButtonToMessageTemplate = u'{0} {1}'

    def renderItem(self, index, text, value, name, cssClass):
        id = '{0}.{1}'.format(name, index)
        elem = renderElement('input',
                             type="checkbox",
                             cssClass=cssClass,
                             name=name,
                             id=id,
                             value=value)

        label = renderElement('label',
                              extra=u'for={0}'.format(id),
                              contents=text)

        return self._joinButtonToMessageTemplate.format(elem, label)

    def renderSelectedItem(self, index, text, value, name, cssClass):
        id = '{0}.{1}'.format(name, index)
        elem = renderElement('input',
                             type="checkbox",
                             cssClass=cssClass,
                             name=name,
                             id=id,
                             value=value,
                             checked="checked")

        label = renderElement('label',
                              extra=u'for={0}'.format(id),
                              contents=text)

        return self._joinButtonToMessageTemplate.format(elem, label)
