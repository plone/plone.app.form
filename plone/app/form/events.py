"""Event definitions
"""

from zope.interface import implements

from zope.component.interfaces import ObjectEvent

from plone.app.form.interfaces import IEditBegunEvent
from plone.app.form.interfaces import IEditCancelledEvent

class EditBegunEvent(ObjectEvent):
    """An edit operation was begun
    """
    implements(IEditBegunEvent)
    
class EditCancelledEvent(ObjectEvent):
    """An edit operation was cancelled
    """
    implements(IEditCancelledEvent)