from urllib.parse import quote_plus, unquote_plus
from pytz import timezone
import arrow
import json
from typing import List, Optional, Union
from typing_extensions import Literal
from pydantic import BaseModel


# {"items": [
#     {
#         "uid": "desktop",
#         "type": "file",
#         "title": "Desktop",
#         "subtitle": "~/Desktop",
#         "arg": "~/Desktop",
#         "autocomplete": "Desktop",
#         "icon": {
#             "type": "fileicon",
#             "path": "~/Desktop"
#         }
#     }
# ]}

OutputType = Optional[Union[Literal['file'], Literal['default']]]


class OutputItem(BaseModel):
    uid: str
    type: OutputType
    title: str
    subtitle: str
    arg: Optional[str]
    autocomplete: Optional[str]


def build_output_item(title: str,
                      subtitle: str,
                      arg: Optional[str] = None,
                      type: OutputType = "default",
                      uid: Optional[str] = None,) -> dict:
    if uid is None:
        uid = title
    return OutputItem(title=title,
                      subtitle=subtitle,
                      arg=arg,
                      type=type,
                      uid=uid
                      ).dict()


def build_output(items: List[dict]):
    if len(items) == 0:
        return json.dumps({'items': [build_output_item('Nothing', '')]})
    return json.dumps({'items': items}, indent=4)


def get_time(event):
    tz_ny = timezone('America/New_York')
    return arrow.get((str(event.startDate()).split(' +')[0])).to(tz_ny)


def encode_arg(arg: str) -> str:
    return quote_plus(str(arg))


def decode_arg(arg: str) -> str:
    return unquote_plus(arg)
