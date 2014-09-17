# -*- coding: utf-8 -*-
"""Event definitions
"""
from plone.app.form.interfaces import IEditBegunEvent
from plone.app.form.interfaces import IEditCancelledEvent
from plone.app.form.interfaces import IEditSavedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class EditBegunEvent(ObjectEvent):
    """An edit operation was begun
    """
    implements(IEditBegunEvent)


class EditCancelledEvent(ObjectEvent):
    """An edit operation was cancelled
    """
    implements(IEditCancelledEvent)


class EditSavedEvent(ObjectEvent):
    """An edit operation was completed
    """
    implements(IEditSavedEvent)
