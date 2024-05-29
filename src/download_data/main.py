# -*- coding: utf-8 -*-
"""
No longer do we wish to download data manually, instead, we will download with a script
"""

import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from datetime import datetime

RAW_DATA_PATH = "tmp/raw"
BASE_URL = "https://yb-big-data-workshop-1.s3-us-west-2.amazonaws.com/index.html"


def get_all_urls():
    data = requests.get(BASE_URL)
    soup = BeautifulSoup(data.text)
    urls = [x["href"] for x in soup.findAll("a")]
    urls = [x for x in urls if x.endswith((".txt", ".txt.gz"))]
    return urls


def url_to_datetime(url: str) -> datetime:
    """
    File paths contain information about the timestamp it was created.
    We want to parse that value.

    Example:
        >>> url = 'https://yb-big-data-workshop-1.s3.amazonaws.com/2024-05-29 18-02-09 measurements.txt'
        >>> url_to_datetime(url)
        ... datetime.datetime(2024, 5, 29, 18, 2, 9)
    """
    pattern = r"s3\.amazonaws\.com/(.*?)\smeasurements"
    raw_date_str = re.search(pattern, url).group(1)
    dt = datetime.strptime(raw_date_str, "%Y-%m-%d %H-%M-%S")

    return dt


def get_data_for_url(url: str, dst_file_name: Path):
    """
    Downloads data from the url (as a stream)
    """
    response = requests.get(url, stream=True)

    # Open a file in binary write mode
    with open(dst_file_name, "wb") as f:
        # Write the response content to the file in chunks
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)


if __name__ == "__main__":
    # urls = get_all_urls()

    url = "https://yb-big-data-workshop-1.s3.amazonaws.com/2024-05-29 18-02-09 measurements.txt"

    dst_dir = Path(RAW_DATA_PATH)
    # Make the directory if you need to
    dst_dir.mkdir(parents=True, exist_ok=True)

    dst_file_name = dst_dir / url.split(".com/")[1]
    if dst_file_name.exists():
        print("already downloaded")
    else:
        get_data_for_url(url, dst_file_name)
