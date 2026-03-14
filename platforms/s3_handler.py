import os
from typing import Any

import boto3
import pickle
from dotenv import load_dotenv


load_dotenv()
bucket_name = os.environ["BUCKET_NAME"]
root_folder = os.environ["ROOT_FOLDER"]
access_key = os.environ["S3_ACCESS_KEY"]
secret_key = os.environ["S3_SECRET_KEY"]
primitives = (bool, str, int, float, type(None))


def s3_resource():
    return boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def s3_client():
    return boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def read_from_s3(path) -> Any:
    client = s3_client()
    response = client.get_object(Key=path, Bucket=bucket_name)
    output = pickle.loads(response["Body"].read())
    return output


def write_to_s3(output: Any, task_id: str, dag_id: str) -> str:
    client = s3_resource()
    data = pickle.dumps(output)
    path = f"{root_folder}/{dag_id}/{task_id}"
    client.Bucket(bucket_name).put_object(Key=path, Body=data)
    return path


def validate_s3_path(path: str, dag_id) -> bool:
    dag_path = f"{root_folder}/{dag_id}"
    if path.startswith(dag_path):
        s3 = s3_client()
        try:
            s3.head_object(Bucket=bucket_name, Key=path)
            return True
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False


def should_write_s3(output: Any) -> bool:
    return type(output) not in primitives

