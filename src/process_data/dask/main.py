# -*- coding: utf-8 -*-
"""
Process the stuff in dask

Resources:
    1. Dask documentation: https://docs.dask.org/en/stable/
"""

import argparse
import time
import dask.dataframe as dd

from src.process_data.base import BaseProcessDataInterface


class DaskInterface(BaseProcessDataInterface):
    """

    Interface for executing dask transformations.


    Use as follows:
        >> df = DaskInterface.in_memory("foo.txt")

    """

    @classmethod
    def in_memory(cls, filename: str) -> dd.DataFrame:
        """
        Process the whole thing in memory

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
        """

        df = (
            dd.read_csv(
                filename,
                sep=";",
                header=None,
                names=["station_name", "measurement"],
            )
            .groupby("station_name")
            .agg(
                min=("measurement", "min"),
                mean=("measurement", "mean"),
                max=("measurement", "max"),
                count=("measurement", "count"),
            )
            .compute()  # don't lazy compute -> compute here
        )

        return df

    @classmethod
    def streaming(cls, filename: str) -> dd.DataFrame:
        """
        API for streaming the data

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
        """
        raise NotImplementedError()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name", default="measurements.txt")
    args = parser.parse_args()

    start = time.time()
    df = DaskInterface().in_memory(args.file_name)

    duration = time.time() - start
    print(f"Duration = {duration: .2f}s")

    print(df.query("station_name == 'Alexandria'").head())
