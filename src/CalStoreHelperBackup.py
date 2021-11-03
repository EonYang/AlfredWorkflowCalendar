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


import time

from CalendarStore import CalCalendarStore, NSDate  # type: ignore


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

    def __updateCalendarsList(self, calendar_names):
        self.calendars = self.store.calendars()
        if calendar_names is None or len(calendar_names) == 0:
            return
        filtered_cals = []
        for cal in self.calendars:
            if cal.title() in calendar_names:
                filtered_cals.append(cal)
        self.calendars = filtered_cals

    def __itemsByCalendar(self, cal_items):
        # get all calendars into a list + collect
        # all items of each calendar into separate lists
        calendars = []
        items_by_cal_uid = {}
        for item in cal_items:
            cal = item.calendar()
            if cal not in calendars:
                calendars.append(cal)
            if not cal.uid() in items_by_cal_uid:
                items_by_cal_uid[cal.uid()] = []
            items_by_cal_uid[cal.uid()].append(item)
        # sort calendars list
        # TODO
        # construct list of dictionaries with keys 'calendar' (the
        # calendar object) and 'items' (all items for that calendar)
        by_cal_list = []
        for calendar in calendars:
            by_cal_list.append({
                'calendar': calendar,
                'items': items_by_cal_uid[calendar.uid()]})
        return by_cal_list

    def __pyDatetimeToNSDate(self, py_datetime):
        if py_datetime is None:
            return None

        if hasattr(
                py_datetime, 'tzinfo') and (
                py_datetime.tzinfo is not None) and (
                py_datetime.tzinfo.utcoffset(py_datetime) is not None):
            # datetime object is 'aware' (has notion of timezone)
            tz_str = py_datetime.strftime('%z')
        else:
            # datetime object is 'naive' (has no notion of timezone)
            # -> use current timezone
            tz_offset_h = time.timezone / 60 / 60 if time.daylight == 0 else \
                time.altzone / 60 / 60
            tz_str = str(abs(tz_offset_h) * 100).rjust(4, '0')
            tz_str = '+' + tz_str if tz_offset_h >= 0 else '-' + tz_str
        # We intentionally reverse the sign of the GMT offset
        # (Python's and Cocoa's notions of it are opposite)
        tz_str = '+' + tz_str[1:] if tz_str[0:1] == '-' else '-' + tz_str[1:]

        # YYYY-MM-DD HH:MM:SS +HHMM
        formatted_datetime_str = py_datetime.strftime('%Y-%m-%d %H:%M:%S ' +
                                                      tz_str)
        return NSDate.dateWithString_(formatted_datetime_str)

    def getEvents(self, calendar_names, start_datetime, end_datetime,
                  by_calendar=False):
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
        self.__updateCalendarsList(calendar_names)
        predicate = \
            CalCalendarStore.eventPredicateWithStartDate_endDate_calendars_(
                start_datetime, end_datetime, self.calendars)
        items = self.store.eventsWithPredicate_(predicate)
        if by_calendar:
            return self.__itemsByCalendar(items)
        return items

    def getUncompletedTasks(self, calendar_names, due_before_date=None,
                            by_calendar=False):
        """
        Returns uncompleted tasks from specified calendars.

        The return value will be a list of Cocoa CalTask objects unless the
        by_calendar argument is set to True, in which case it will be a list
        of dictionaries, each with the keys 'calendar' (pointing to a Cocoa
        CalCalendar object) and 'events' (pointing to a list of Cocoa CalTask
        objects, each from that calendar).

        Positional arguments:
        calendar_names -- A list containing the names of the calendars
                          to get the tasks from, or None to get tasks from
                          all calendars.

        Keyword arguments:
        due_before_date -- The due date cut-off for returned tasks. If this
                           argument is set, only tasks that are due before
                           the given date are returned.
        by_calendar -- Whether to separate the returned tasks by calendar.

        """
        self.__updateCalendarsList(calendar_names)
        # taskPredicateWithUncompletedTasksDueBefore_calendars_() hangs if the
        # given date is a Python datetime object instead of an NSDate object
        if due_before_date is not None:
            due_before_nsdate = self.__pyDatetimeToNSDate(due_before_date)
            predicate = \
                CalCalendarStore.\
                taskPredicateWithUncompletedTasksDueBefore_calendars_(
                    due_before_nsdate, self.calendars)
        else:
            predicate = CalCalendarStore.taskPredicateWithUncompletedTasks_(
                self.calendars)
        items = self.store.tasksWithPredicate_(predicate)
        if by_calendar:
            return self.__itemsByCalendar(items)
        return items
