from sys import argv
from CalStoreHelper import CalStoreHelper
from Foundation import NSDate  # type: ignore
import arrow
from pytz import timezone
from utils import build_output_item, build_output
days = int(argv[1] if len(argv) > 1 else '3')

tz_ny = timezone('America/New_York')
helper = CalStoreHelper()

res = helper.getEvents(
    None,
    NSDate.date(),
    NSDate.dateWithTimeIntervalSinceNow_(3600 * 24 * days)
)


def subtitle(event):
    time = arrow.get((str(event.startDate()).split(' +')[0])).to(tz_ny)
    return "{} | {} | {}".format(
        time.humanize(),
        time.format('hh:mm A'),
        event.calendar().title(),
    )


def notes(event):
    return event.notes()


print(build_output(
    [build_output_item(
        event.title(),
        subtitle(event),
        notes(event),
        uid=event.uid())
        for event in res]))
