import os
from typing import Any

import boto3
import pickle
from dotenv import load_dotenv

from basics.task import Task

load_dotenv()
s3_root_folder = os.environ["S3_FOLDER"]


def s3_connection():
    access_key = os.environ["S3_ACCESS_KEY"]
    secret_key = os.environ["S3_SECRET_KEY"]
    return boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def read_from_s3(path):
    pass


def write_to_s3(output: Any, task_id: str, dag_id: str) -> str:
    client = s3_connection()
    data = pickle.dumps(output)
    path = f"{dag_id}/{task_id}"
    client.Bucket(s3_root_folder).put_object(Key=path, Body=data)
    return f"{s3_root_folder}/{path}"


def validate_s3_path(path: str) -> bool:
    pass


write_to_s3({"name":"noa", "age": 18}, "dag12", "task12")
