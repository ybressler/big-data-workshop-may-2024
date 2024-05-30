# -*- coding: utf-8 -*-
"""
Process the stuff in polars

Resources:
    1. Polars documentation: https://docs.pola.rs/
"""

import argparse
import time
from functools import partial

import polars as pl

from src.process_data.base import BaseProcessDataInterface


class PolarsInterface(BaseProcessDataInterface):
    """
    Interface for executing polars transformations.

    Use as follows:
        >> df = PolarsInterface.in_memory("foo.txt")

    """

    @classmethod
    def in_memory(cls, filename: str) -> pl.DataFrame:
        """
        Process the whole thing in memory

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
        """
        if filename.endswith((".csv", ".txt")):
            loader = partial(pl.read_csv, separator=";", has_header=False, new_columns=["station_name", "measurement"])
        elif filename.endswith(".parquet"):
            loader = pl.read_parquet

        df = (
            loader(filename)
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

        # Can't open a compressed file in context, otherwise, will need to load all data in memory
        # issue: https://github.com/pola-rs/polars/issues/7287
        # Workaround -> compress to parquet
        return (
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

    @classmethod
    def streaming_parquet(cls, filename: str) -> pl.DataFrame:
        """
        Duplicate method, to make it easier for people to understand.
        """
        return (
            pl.scan_parquet(
                filename,
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name", default="measurements.txt")
    args = parser.parse_args()

    start = time.time()
    if args.file_name.endswith((".csv", ".txt")):
        df = PolarsInterface().streaming(args.file_name)
    else:
        df = PolarsInterface().streaming_parquet(args.file_name)

    duration = time.time() - start
    print(f"Duration = {duration: .2f}s")
    print(df.filter(pl.col("station_name") == "Alexandria").head())
