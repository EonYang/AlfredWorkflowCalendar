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


def subtitle(event, *other_info: str):
    time = get_time(event)
    return '{:20s} \t{:20s} \t{:32s}'.format(
        time.humanize(),
        time.format('MM-DD hh:mm A'),
        event.calendar().title(),
    ) + "\t|\t".join([
        *other_info
    ]
    )


def notes(event):
    return event.notes()


print(build_output(
    [build_output_item(
        event.title(),
        subtitle(event),
        encode_arg(notes(event)))
        for order, event in enumerate(res)]))
