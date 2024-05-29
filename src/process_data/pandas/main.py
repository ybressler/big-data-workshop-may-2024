# -*- coding: utf-8 -*-
"""
Process the stuff in pandas
"""
import numpy as np
import pandas as pd


class PandasThing:
    @classmethod
    def in_memory(cls, filename: str):
        """
        Load the whole file in memory
        """
        df = pd.read_csv(filename, sep=";", header=None, names=["station_name", "measurement"])
        df_agg = (
            df.groupby("station_name")
            .agg({"measurement": ["min", "mean", "max"]})
            .query("station_name == 'Alexandria'")
        )

        return df_agg

    @classmethod
    def in_chunks(cls, filename: str, chunksize: int = 100_000):
        """
        Process parts of the file, then concat results
        """

        df_result = pd.DataFrame()

        # # merge previously aggregated DF with a new portion of data and aggregate it again
        # df = (pd.concat([df,
        #                  chunk.groupby('Geography')['Count'].sum().to_frame()])
        #       .groupby(level=0)['Count']
        #       .sum()
        #       .to_frame()
        #       )
        lazy_df = pd.read_csv(
            filename, sep=";", header=None, names=["station_name", "measurement"], chunksize=chunksize
        )
        for chunk in lazy_df:
            df_agg = (
                chunk.groupby("station_name", as_index=True)
                .agg(
                    min=("measurement", "min"),
                    mean=("measurement", "mean"),
                    max=("measurement", "max"),
                    count=("measurement", "count"),
                )
                .query("station_name == 'Alexandria'")
            )

            df_result = pd.concat(
                [df_result, df_agg]
            )  # .groupby(level=0)["count"].agg({"measurement": ["min", "mean", "max", "count"]})
            # df_result.columns = ["min", "mean", "max", "count"]
            # Take the avg between rows
            # df_result = df_result.groupby(level=0).agg(
            #     {
            #         "min": min,
            #         "max": max,
            #         "count": "count",
            #         "mean": lambda s: sum(s['count'] * s['mean']) / sum(s['count']),
            #     }
            # )
        def calc_mean():
            ...
        # Now aggregate at the end (count * mean / count)
        # tmp = df_result.groupby(level=0).agglambda s: pd.Series({
        #     "corr(x, y)": np.corrcoef(s["x"], s["y"]),
        #     "corr(x, z)": np.corrcoef(s["x"], s["z"]),
        # })

        df_result = df_result.groupby(level=0).agg(
            min=("min", "min"),
            max=("max", "max"),
            count=("count", "sum"),
        )

        return df_result


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Analyze measurement file")
    # parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name")
    # args = parser.parse_args()
    file_name = "src/create_data/tmp/measurements.txt"
    df = PandasThing.in_chunks(file_name)
    z = df.head()
