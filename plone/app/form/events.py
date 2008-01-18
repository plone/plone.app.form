"""Event definitions
"""

from zope.interface import implements

from zope.app.event.objectevent import ObjectEvent

from plone.app.form.interfaces import IEditBegunEvent
from plone.app.form.interfaces import IEditCancelledEvent
from plone.app.form.interfaces import IEditSavedEvent

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
