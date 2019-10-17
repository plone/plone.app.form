# -*- coding: utf-8 -*-
"""Event definitions
"""
from plone.app.form.interfaces import IEditBegunEvent
from plone.app.form.interfaces import IEditCancelledEvent
from plone.app.form.interfaces import IEditSavedEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implementer


class EditBegunEvent(ObjectEvent):
    """An edit operation was begun
    """
    implementer(IEditBegunEvent)


class EditCancelledEvent(ObjectEvent):
    """An edit operation was cancelled
    """
    implementer(IEditCancelledEvent)


class EditSavedEvent(ObjectEvent):
    """An edit operation was completed
    """
    implementer(IEditSavedEvent)
