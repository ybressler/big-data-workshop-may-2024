# -*- coding: utf-8 -*-
"""
Process the stuff in pandas
"""

import pandas as pd
import argparse


def do_thing(filename: str):
    df = pd.read_csv(filename, sep=";", header=None, names=["station_name", "measurement"])
    print(df.head(2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name")
    args = parser.parse_args()

    df = do_thing(args.file_name)
