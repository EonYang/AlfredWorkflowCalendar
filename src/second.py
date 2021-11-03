# import json
from utils import decode_arg
from utils import build_output_item, build_output
from sys import argv
input = decode_arg(argv[1])


def extract_urls(input):
    lines = [x for x in input.split('\n') if len(x) > 0]
    result = []
    for i, line in enumerate(lines):
        if 'http' in line:
            title = lines[i - 1] if i > 0 else 'unknown'
            url = line
            result.append((title, url))
    return result
# breakpoint()


lines = extract_urls(input)

print(build_output(
    [build_output_item(
        title,
        url,
        url,
        uid=str(i))
        for i, (title, url) in enumerate(lines)]))
