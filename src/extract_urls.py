import re
from sys import argv, stdout
from typing import List
from utils import build_output_item, build_output
notes = argv[1] if len(argv) > 1 else 'No notes found'


def extract_urls(text: str) -> List[str]:
    return re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text)


urls = extract_urls(notes)
items = [build_output_item(url, '', url) for url in urls]

stdout.write(build_output(items))
