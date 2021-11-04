from sys import argv
from CalStoreHelper import CalStoreHelper
from Foundation import NSDate  # type: ignore
from utils import encode_arg
from utils import get_time

from utils import build_output_item, build_output
days = int(argv[1] if len(argv) > 1 else '3')


helper = CalStoreHelper()

res = helper.getEvents(
    NSDate.date(),
    NSDate.dateWithTimeIntervalSinceNow_(3600 * 24 * days)
)

res.sort(key=lambda event: get_time(event))


def subtitle(event):
    time = get_time(event)
    return " | ".join([
        time.humanize(),
        time.format('MM-DD hh:mm A'),
        event.calendar().title(),
    ]
    )


def notes(event):
    return event.notes()


print(build_output(
    [build_output_item(
        event.title(),
        subtitle(event),
        encode_arg(notes(event)),
    )
        for event in res]))
