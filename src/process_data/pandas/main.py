# -*- coding: utf-8 -*-
"""
Process the stuff in pandas
"""

import argparse
import time
import pandas as pd
from parallel_pandas import ParallelPandas


class PandasThing:
    """
    Interface for executing pandas transformations.

    Use as follows:
        >> df = PandasThing.in_memory("foo.txt")

    Alternatively, enable parallel processing
        >> df = PandasThing(parallel = True).in_memory("foo.txt")

    However, initializing with parallel processing won't really affect us,
    since most of our data processing is IO bound.
    """

    def __init__(self, parallel: bool = False):
        if parallel:
            # initialize parallel-pandas
            ParallelPandas.initialize(n_cpu=8, split_factor=2)

    @classmethod
    def in_memory(cls, filename: str) -> pd.DataFrame:
        """
        Load the whole file in memory
        """
        df = pd.read_csv(filename, sep=";", header=None, names=["station_name", "measurement"])
        df_agg = df.groupby("station_name").agg({"measurement": ["min", "mean", "max"]})

        return df_agg

    @classmethod
    def in_chunks(cls, filename: str, chunksize: int = 1_000_000) -> pd.DataFrame:
        """
        Process parts of the file, concat results, and continue

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
            chunksize: Number of rows to be read per iteration. (Reduce load on memory)
        """

        df_result = pd.DataFrame()

        # merge previously aggregated DF with a new portion of data and aggregate it again
        lazy_df = pd.read_csv(
            filename, sep=";", header=None, names=["station_name", "measurement"], chunksize=chunksize
        )
        for chunk in lazy_df:
            df_agg = chunk.groupby("station_name", as_index=True).agg(
                min=("measurement", "min"),
                mean=("measurement", "mean"),
                max=("measurement", "max"),
                count=("measurement", "count"),
            )

            # Calculate the mean
            df_result = (
                pd.concat([df_result, df_agg])
                .groupby(level=0)
                .apply(
                    lambda s: pd.Series(
                        {
                            "min": s["min"].min(),
                            "mean": (s["count"] * s["mean"]).sum() / s["count"].sum(),  # sum(n * mean) / sum(n)
                            "max": s["max"].max(),
                            "count": s["count"].sum(),
                        }
                    )
                )
            )

        return df_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name", default="measurements.txt")
    args = parser.parse_args()

    start = time.time()
    df = PandasThing().in_chunks(args.file_name, chunksize=10_000_000)

    duration = time.time() - start
    print(f"Duration = {duration: .2f}s")
    print(df.query("station_name == 'Alexandria'").head())
