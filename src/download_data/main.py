# -*- coding: utf-8 -*-
"""
No longer do we wish to download data manually, instead, we will download with a script
"""

import shutil
from typing import List
import re
from pathlib import Path

import polars as pl
import requests
from pgzip import pgzip
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime

RAW_DATA_PATH = "tmp/raw"
BASE_URL = "https://yb-big-data-workshop-1.s3-us-west-2.amazonaws.com/index.html"


def get_all_urls() -> List[str]:
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


# def url_to_file_name(url: str) -> str:
#     """Extract filename from the url"""


def get_data_for_url(url: str, dst_file_name: Path):
    """
    Downloads data from the url (as a stream)

    NOTE:
        We could decompress as we download and that would be ideal, but let's keep
        things simple for now
    """
    response = requests.get(url, stream=True)
    # Sizes in bytes.
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    # Open a file in binary write mode
    with tqdm(
        total=total_size, unit="B", unit_scale=True, desc=f"Downloading data from url {url}"
    ) as progress_bar, open(dst_file_name, "wb") as f:
        # Write the response content to the file in chunks
        for chunk in response.iter_content(chunk_size=block_size):
            progress_bar.update(len(chunk))
            f.write(chunk)


def decompress_file(file_name: Path, with_progress: bool = False):
    """Decompress a file, choose if you want a progress bar or not"""
    # Determine the output file name by removing the ".gz" extension
    output_file_name = file_name.with_suffix("")

    if with_progress:
        return decompress_file_with_progress_bar(file_name)
    else:
        with pgzip.open(file_name, "rb") as f_in, open(output_file_name, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def decompress_file_with_progress_bar(file_name: Path):
    """
    Decompresses and shows progress. Pretty neat.
    """
    total_size = file_name.stat().st_size * 3

    # Determine the output file name by removing the ".gz" extension
    output_file_name = file_name.with_suffix("")

    chunk_size = 1024
    # With progress bar
    with tqdm(total=total_size, unit="B", unit_scale=True, desc=f"Decompressing {file_name}") as progress_bar:
        with pgzip.open(file_name, "rb") as f_in, open(output_file_name, "wb") as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                f_out.write(chunk)
                progress_bar.update(len(chunk))


def convert_txt_to_parquet(file_name: Path, dst_file_name: Path) -> Path:
    """Convert txt data to parquet format"""

    df = pl.read_csv(file_name, separator=";", has_header=False, new_columns=["station_name", "measurement"])
    df.write_parquet(dst_file_name)


if __name__ == "__main__":
    # urls = get_all_urls()
    urls = []

    dst_dir = Path(RAW_DATA_PATH)
    # Make the directory if you need to
    dst_dir.mkdir(parents=True, exist_ok=True)

    for i, url in enumerate(urls):
        if i >= 3:
            pass  # switch to `break` if you want to test it out for 1 url

        dst_file_name = dst_dir / url.split(".com/")[1]
        if dst_file_name.exists():
            print(f"already downloaded '{url}'")
        else:
            get_data_for_url(url, dst_file_name)

    # Now, iterate over the directory and decompress files
    for file_name in dst_dir.iterdir():
        if file_name.suffix != ".gz":
            continue
        dst_file_name = file_name.with_suffix("")
        if dst_file_name.exists():
            print(f"already decompressed '{file_name}'")
        else:
            decompress_file(file_name, True)

    # now convert to parquet
    for file_name in dst_dir.iterdir():
        if file_name.suffix != ".txt":
            continue

        new_parts = ["clean" if x == "raw" else x for x in file_name.parts]
        dst_file_name = Path(*new_parts).with_suffix(".parquet")
        dst_file_name.parent.mkdir(parents=True, exist_ok=True)

        if dst_file_name.exists():
            print(f"already converted '{file_name}' to parquet --> {dst_file_name}")
        else:
            parquet_file = convert_txt_to_parquet(file_name, dst_file_name)
            print(f"finished converting '{file_name}' to parquet --> {dst_file_name}")
