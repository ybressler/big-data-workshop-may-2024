# -*- coding: utf-8 -*-
import os
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Set

import boto3
from boto3.s3.transfer import MB, S3Transfer, TransferConfig


class ProgressPercentage(object):
    """Enabled progress bar on multipart upload"""

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self.batches = max(8 * MB // self._size, 1)

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write("\r%s  %s / %s  (%.2f%%)" % (self._filename, self._seen_so_far, self._size, percentage))
            sys.stdout.flush()


class ServiceBase:
    """Base class for interacting with S3"""

    bucket_name: str

    def __init__(self, s3_client: boto3.client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload_to_s3(self, data: bytes, file_name: str):
        return self.s3_client.put_object(Bucket=self.bucket_name, Body=data, Key=file_name)

    def upload_file(self, file_name: Path, with_percentage: bool = False):
        dt_prefix = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H-%M-%S")

        extra_args = {}
        # prints progress with percentage
        if with_percentage:
            extra_args["callback"] = ProgressPercentage(file_name)

        transfer = S3Transfer(
            self.s3_client,
            # trying to boost performance with these configs (requires some tinkering)
            config=TransferConfig(multipart_threshold=16 * MB, multipart_chunksize=16 * MB, max_concurrency=200),
        )

        return transfer.upload_file(file_name, self.bucket_name, f"{dt_prefix} {file_name.name}", **extra_args)

    def remove_s3_file(self, file_name: str):
        return self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def get_existing_s3_files(self) -> Set[str]:
        """
        Returns the files which currently exist in S3
        """
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        return {x["Key"] for x in response["Contents"]}
