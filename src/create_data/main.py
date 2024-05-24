# -*- coding: utf-8 -*-
"""
Entrypoint for program which generates data
"""

import datetime

import boto3
from pathlib import Path

from src.create_data.base import ServiceBase
from src.create_data.create_measurements import CreateMeasurement

DATA_SOURCE_S3_BUCKET = "yb-big-data-workshop-1"


if __name__ == "__main__":
    s3_client = boto3.Session(profile_name="yb-personal").client("s3")
    s3_service = ServiceBase(s3_client=s3_client, bucket_name=DATA_SOURCE_S3_BUCKET)

    file_name = Path("tmp/measurements.txt.gz")
    # Make the directory if you need to
    file_name.parent.mkdir(parents=True, exist_ok=True)

    measurement = CreateMeasurement()
    measurement.generate_measurement_file(file_name=file_name.as_posix(), records=1_0_000_000, compressed=True)
    print("finished generating the data")

    dt_start = datetime.datetime.now()
    res = s3_service.upload_file(file_name)
    dt_end = datetime.datetime.now()

    duration = (dt_end - dt_start).total_seconds()
    print(f"finished uploading the data to S3, took {duration:,} seconds")

    file_name.unlink()
    print("finished deleting the data locally")
