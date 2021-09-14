import itertools
import os
from urllib.parse import urlparse

import requests


CURRENT_DIR = os.getcwd()


def get_file_name(url, extension='.html'):
    start_not_empty = 1
    parse_result = urlparse(url)
    splitted_netloc = parse_result.netloc.split(".")
    splitted_path = parse_result.path.split("/")[start_not_empty:]
    file_name = "-".join(itertools.chain(splitted_netloc, splitted_path))
    return file_name + extension


def download(url, output_dir=CURRENT_DIR):
    file_name = get_file_name(url)
    file_path = os.path.join(output_dir, file_name)
    response = requests.get(url)
    return write_to_file(file_path, response.text)


def write_to_file(path, file_data):
    with open(path, "w") as f:
        f.write(file_data)
    return path
