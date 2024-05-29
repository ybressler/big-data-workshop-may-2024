# -*- coding: utf-8 -*-
"""
Process the stuff in pandas
"""

import argparse
import time
import polars as pl


class PolarsThing:
    """
    Interface for executing polars transformations.

    Use as follows:
        >> df = PolarsThing.in_memory("foo.txt")

    """

    @classmethod
    def in_memory(cls, filename: str) -> pl.DataFrame:
        """
        Process the whole thing in memory

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
        """

        # Can't open in context, otherwise, will need to load all data in memory...
        df = (
            pl.read_csv(
                filename,
                separator=";",
                has_header=False,
                new_columns=["station_name", "measurement"],
            )
            .group_by("station_name")
            .agg(
                pl.min("measurement").alias("min_measurement"),
                pl.mean("measurement").alias("mean_measurement"),
                pl.max("measurement").alias("max_measurement"),
            )
            .sort("station_name")
        )

        return df

    @classmethod
    def streaming(cls, filename: str) -> pl.DataFrame:
        """
        API for streaming the data

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
        """

        # Can't open in context, otherwise, will need to load all data in memory...
        df = (
            pl.scan_csv(
                filename,
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

        return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name", default="measurements.txt")
    args = parser.parse_args()

    start = time.time()
    df = PolarsThing().in_memory(args.file_name)

    duration = time.time() - start
    print(f"Duration = {duration: .2f}s")
    print(df.filter(pl.col("station_name") == "Alexandria").head())
