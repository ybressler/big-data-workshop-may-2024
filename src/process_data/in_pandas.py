# -*- coding: utf-8 -*-
"""
Process the stuff in pandas
"""

import argparse


def do_thing(filename: str): ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze measurement file")
    parser.add_argument("-f", "--file_name", dest="file_name", type=str, help="File name")
    args = parser.parse_args()

    df = do_thing(args.file_name)
