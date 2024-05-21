# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from typing import Set

import boto3
from boto3.s3.transfer import MB, TransferConfig


class ServiceBase:
    """Base class for interacting with S3"""

    bucket_name: str

    def __init__(self, s3_client: boto3.client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload_to_s3(self, data: bytes, file_name: str):
        return self.s3_client.put_object(Bucket=self.bucket_name, Body=data, Key=file_name)

    def upload_file(self, file_name: str):
        dt_prefix = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H-%M-%S")
        return self.s3_client.upload_file(
            Filename=file_name,
            Bucket=self.bucket_name,
            Key=f"{dt_prefix} measurements.txt",
            # trying to boost performance with these configs
            Config=TransferConfig(multipart_threshold=8 * MB, multipart_chunksize=8 * MB, max_concurrency=50),
        )

    def remove_s3_file(self, file_name: str):
        return self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def get_existing_s3_files(self) -> Set[str]:
        """
        Returns the files which currently exist in S3
        """
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        return {x["Key"] for x in response["Contents"]}
