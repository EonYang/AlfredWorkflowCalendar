#
# The MIT License
#
# Copyright (c) 2010 Ali Rantakari - http://hasseg.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
This is the CalStoreHelper module. It contains the
CalStoreHelper class.

Copyright 2010 Ali Rantakari - http://hasseg.org

"""


from CalendarStore import CalCalendarStore  # type: ignore


class CalStoreHelper(object):
    """
    This class provides helper methods for getting tasks or events
    from the OS X calendar store.

    Note that the returned data will contain Cocoa CalendarStore framework
    objects obtained through the Scripting Bridge. Refer to Apple's
    documentation to see what properties are available in the returned
    objects (and note that these properties will actually be methods in
    Python, e.g. you would call the startDate() method of a CalEvent object
    to get its startDate).

    http://tinyurl.com/calendarstore-api-docs
    [developer.apple.com]

    """

    def __init__(self):
        self.store = CalCalendarStore.defaultCalendarStore()
        if self.store is None:
            raise Exception('The default calendar store returns None')
        self.calendars = None

    def getEvents(self,  start_datetime, end_datetime, ):
        """
        Returns events between a specified time span from specified calendars.

        The return value will be a list of Cocoa CalEvent objects unless the
        by_calendar argument is set to True, in which case it will be a list
        of dictionaries, each with the keys 'calendar' (pointing to a Cocoa
        CalCalendar object) and 'events' (pointing to a list of Cocoa CalEvent
        objects, each from that calendar).

        Positional arguments:
        calendar_names -- A list containing the names of the calendars
                          to get the events from, or None to get events from
                          all calendars.
        start_datetime -- The start datetime for the time span between which
                          to get events.
        end_datetime -- The end datetime for the time span between which to
                        get events.

        Keyword arguments:
        by_calendar -- Whether to separate the returned events by calendar.

        """
        self.calendars = self.store.calendars()
        predicate = \
            CalCalendarStore.eventPredicateWithStartDate_endDate_calendars_(
                start_datetime, end_datetime, self.calendars)
        items = self.store.eventsWithPredicate_(predicate)
        return items
