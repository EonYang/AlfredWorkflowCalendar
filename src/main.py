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
res = [(i, e) for i, e in enumerate(res)]


def subtitle(event, order):
    time = get_time(event)
    return " | ".join([
        time.humanize(),
        time.format('MM-DD hh:mm A'),
        event.calendar().title(),
        str(order)
    ]
    )


def notes(event):
    return event.notes()


print(build_output(
    [build_output_item(
        event.title(),
        subtitle(event, order),
        encode_arg(notes(event)),
        uid=event.uid())
        for order, event in res]))
