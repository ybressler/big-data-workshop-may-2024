# -*- coding: utf-8 -*-
from typing import Set

import boto3
import httpx

headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
}


class ServiceBase:
    """Base class for interacting with S3"""

    bucket_name: str

    def __init__(self, s3_client: boto3.client):
        self.s3_client = s3_client
        self.request_session = httpx.Client(headers=headers)

    def upload_to_s3(self, data: bytes, file_name: str):
        """
        ToDo: Allow multi-part upload for very large files
        """
        return self.s3_client.put_object(Bucket=self.bucket_name, Body=data, Key=file_name)

    def remove_s3_file(self, file_name: str):
        return self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def get_existing_s3_files(self) -> Set[str]:
        """
        Returns the files which currently exist in S3
        """
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        return {x["Key"] for x in response["Contents"]}
