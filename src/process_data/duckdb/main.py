# -*- coding: utf-8 -*-
"""
Process the stuff in duckdb

Resources:
    1. DuckDB documentation: ...
"""

import argparse
import time

import duckdb
import pandas as pd

from src.process_data.base import BaseProcessDataInterface


class DuckDBInterface(BaseProcessDataInterface):
    """
    Interface for executing duckDB transformations.

    Use as follows:
        >> df = DuckDBInterface.in_memory("foo.txt")

    """

    @classmethod
    def in_memory(cls, filename: str) -> pd.DataFrame:
        """
        Process the whole thing in memory

        Args:
            filename: Name of the file. Should be relative path to the location where
                this script is invoked.
        """

        with duckdb.connect() as conn:
            data = conn.sql(f"""
                select
                    station_name,
                    min(measurement) as min_measurement,
                    cast(avg(measurement) as decimal(8, 1)) as mean_measurement,
                    max(measurement) as max_measurement
                from read_csv(
                    "{filename}",
                    header=false,
                    columns={{'station_name': 'varchar', 'measurement': 'decimal(8, 1)'}},
                    delim=';',
                    parallel=true
                )
                group by station_name
                order by station_name
            """)

            return data.df()

    @classmethod
    def streaming(cls, filename: str):
        raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name", default="measurements.txt")
    args = parser.parse_args()

    start = time.time()
    df = DuckDBInterface().in_memory(args.file_name)

    duration = time.time() - start
    print(f"Duration = {duration: .2f}s")
    print(df.query("station_name == 'Alexandria'").head())
