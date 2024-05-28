# -*- coding: utf-8 -*-
"""
Process a measurements file:
    1. Get data from URL
    2. If compressed, decompress
        - check first if already decompressed (no need to reprocess)
    3. Parse date from file name
    4. Calculate result
    5. Store result in new file

Code credits: https://github.com/ifnesi/1brc#submitting
"""

import argparse
import shutil

import polars as pl
from pgzip import pgzip


def do_thing(file_name: str):
    """Processes file"""

    new_file_name = file_name.replace(".gz", "")

    with pgzip.open(file_name, "rb") as f_in, open(file_name.replace(".gz", ""), "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    # Can't open in context, otherwise, will need to load all data in memory...
    df = (
        pl.scan_csv(
            new_file_name,
            separator=";",
            has_header=False,
            with_column_names=lambda cols: ["station_name", "measurement"],
        )
        .group_by("station_name")
        .agg(
            pl.min("measurement").alias("min_measurement"),
            pl.mean("measurement").alias("mean_measurement"),
            pl.max("measurement").alias("max_measurement"),
        )
        .sort("station_name")
        .collect(streaming=True)
    )

    df.write_csv(new_file_name.replace(".txt", "") + " - results.csv", separator=",")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name")
    args = parser.parse_args()

    df = do_thing(args.file_name)
