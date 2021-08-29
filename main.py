from sys import argv
from CalStoreHelper import CalStoreHelper
from Foundation import NSDate  # type: ignore
import arrow
import json
days = int(argv[1] if len(argv) > 1 else '3')

helper = CalStoreHelper()

res = helper.getEvents(
    ['yy2473@nyu.edu'],
    NSDate.date(),
    NSDate.dateWithTimeIntervalSinceNow_(3600 * 24 * days)
)


def buildOutputItem(event):
    return {
        "uid": event.uid(),
        "type": "default",
        "title": event.title(),
        "subtitle": f"{arrow.get((str(event.startDate()).split(' +')[0])).humanize()} | {event.calendar().title()}",  # noqa: E501
        "icon": {
            'path': './icon.png'
        }
    }


print(json.dumps({
    'items': [buildOutputItem(event) for event in res]
}))
