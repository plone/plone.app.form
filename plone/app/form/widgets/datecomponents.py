from time import localtime

from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from DateTime.DateTime import DateTimeError
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from interfaces import IDateComponents

CEILING=DateTime(9999, 0)
FLOOR=DateTime(1970, 0)
PLONE_CEILING=DateTime(2021,0) # 2020-12-31


class DateComponents(BrowserView):
    """A view that provides some helper methods useful in date widgets.
    """

    implements(IDateComponents)

    def result(self, date=None,
               use_ampm=False,
               starting_year=None,
               ending_year=None,
               future_years=None,
               minute_step=5):
        """Returns a dict with date information.
        """
        ptool = getToolByName(self.context, 'portal_properties')

        site_props = ptool.site_properties

        # Get the date format from the locale
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')

        dates = portal_state.locale().dates

        timepattern = dates.getFormatter('time').getPattern()
        if 'a' in timepattern:
             use_ampm = True

        # 'id' is what shows up. 
        # 'value' is the value for the form.
        # 'selected' is whether or not it is selected.

        default=0
        years=[]
        hours=[]
        minutes=[]
        ampm=[]
        now=DateTime()

        if isinstance(date, basestring):
            date=date.strip()
            if not date:
                date=None

        if date is None:
            date=now
            default=1
        elif not isinstance(date, DateTime):
            try:
                date=DateTime(date)
            except (TypeError, DateTimeError):
                date=now
                default=1

        # Anything above PLONE_CEILING should be PLONE_CEILING
        if date.greaterThan(PLONE_CEILING):
            date = PLONE_CEILING

        # Represent the date in the local timezone
        try:
            local_zone = date.localZone(localtime(date.timeTime()))
        except ValueError:
            # Dates before 1970 use a negative timeTime() value, which on
            # on some platforms are not handled well and lead to a ValueError.
            # In those cases, calculate the local timezone (which is DST based)
            # from the same date in the *current year* instead. This is better
            # than failing altogether!
            timeZoneDate = DateTime(localtime().tm_year, *date.parts()[1:])
            local_zone = date.localZone(localtime(timeZoneDate.timeTime()))
        date = date.toZone(local_zone)

        # Get portal year range
        if starting_year is None:
            min_year = site_props.getProperty('calendar_starting_year', 1999)
        else:
            min_year = int(starting_year)
        if ending_year is None:
            if future_years is None:
                max_year = site_props.getProperty('calendar_future_years_available', 5) + now.year()
            else:
                max_year = int(future_years) + now.year()
        else:
            max_year = int(ending_year)

        # keeps the existing date if it's out of range
        if not default:
            if min_year > date.year():
                min_year = date.year()
            if max_year < date.year():
                max_year = date.year()
        years = [min_year, max_year]

        if use_ampm:
            hours_range=[12]+range(1,12)
            hour_default='12'
            hour=int(date.h_12())
        else:
            hours_range=range(0,24)
            hour_default='00'
            hour=int(date.h_24())
        
        if default:
            hours.append({'id': '--', 'value': hour_default, 'selected': 1})
        else:
            hours.append({'id': '--', 'value': hour_default, 'selected': None})

        for x in hours_range:
            d={'id': '%02d' % x, 'value': '%02d' % x, 'selected': None }
            if x==hour and not default:
                d['selected']=1
            hours.append(d)

        if default:
            minutes.append({'id': '--', 'value': '00', 'selected': 1})
        else:
            minutes.append({'id': '--', 'value': '00', 'selected': None})
            
        minute=int(date.strftime('%M'))
        
        if minute + minute_step >= 60:
            # edge case. see doctest for explanation
            minute = 60 - minute_step

        for x in range(0, 60, minute_step):
            d={'id': '%02d' % x, 'value': '%02d' % x, 'selected': None}
            if (x==minute or minute < x < minute+minute_step) and not default:
                d['selected']=1
            minutes.append(d)

        if use_ampm:
            p=date.strftime('%p')

            if default:
                ampm.append({'id': '--', 'value': 'AM', 'selected': 1})
            else:
                ampm.append({'id': '--', 'value': 'AM', 'selected': None})

            for x in ('AM', 'PM'):
                d={'id': x, 'value': x, 'selected': None}
                if x==p and not default:
                    d['selected']=1
                ampm.append(d)

        return {'years': years, 'date': date.strftime('%Y-%m-%d'),
                'hours': hours, 'minutes': minutes, 'ampm': ampm}
