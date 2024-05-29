# -*- coding: utf-8 -*-
import argparse

import polars as pl


def process_non_compressed_file(file_name: str):
    """Processes file"""

    # Can't open in context, otherwise, will need to load all data in memory...
    df = (
        pl.scan_csv(
            file_name,
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

    results_file_name = file_name.replace(".txt", "") + " - results.csv"
    print(f"Writing results to {results_file_name}")
    df.write_csv(results_file_name, separator=",")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name")
    args = parser.parse_args()

    df = process_non_compressed_file(args.file_name)
