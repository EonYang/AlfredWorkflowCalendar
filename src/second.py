# import json
from typing import Optional, Tuple
from utils import decode_arg
from utils import build_output_item, build_output
from sys import argv

input: str = decode_arg(argv[1])


def extract_title_url_in_line(line: str) -> Tuple[Optional[str], str]:
    parts = line.split()
    j = 0
    while j < len(parts) and not parts[j].startswith('http'):
        j += 1
    if j < len(parts):
        title = ' '.join(parts[:j])
        url = parts[j]
        return title, url
    else:
        return None, line


def extract_urls(input: str):
    lines = [x for x in input.split('\n') if len(x) > 0]
    result = []
    for i, line in enumerate(lines):
        if 'http' in line:
            if line.startswith('http'):
                title = lines[i - 1] if i > 0 else 'unknown'
                url = line
                result.append((title, url))
            else:
                title, url = extract_title_url_in_line(line)
                if title is None:
                    title = lines[i - 1] if i > 0 else 'unknown'
                result.append((title, url))
    return result


lines = extract_urls(input)

print(build_output(
    [build_output_item(
        title,
        url,
        url,
        uid=str(i))
        for i, (title, url) in enumerate(lines)]))
