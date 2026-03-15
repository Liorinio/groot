import os
import boto3
import pickle
from typing import Any
from dotenv import load_dotenv


load_dotenv()
bucket_name = os.environ["BUCKET_NAME"]
root_folder = os.environ["ROOT_FOLDER"]
access_key = os.environ["S3_ACCESS_KEY"]
secret_key = os.environ["S3_SECRET_KEY"]
primitives = (bool, str, int, float, type(None))


def s3_client():
    """
    This function connects to the s3 client with the global credentials read from a .env file
    """
    return boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)


def read_from_s3(path) -> Any:
    """
    This function reads the content in the s3 path provided,
    it should be under the global bucket name and root folder
    returns the value she read unpickled
    """
    client = s3_client()
    response: dict = client.get_object(Key=path, Bucket=bucket_name)
    output: Any = pickle.loads(response["Body"].read())
    client.close()
    return output


def write_to_s3(output: Any, task_id: str, dag_id: str) -> str:
    """
    this function writes to s3 in the path of dag_id/task_id within the root path provided in the .env file,
    returns the path which she wrote to using a pickle file
    """
    client = s3_client()
    data: bytes = pickle.dumps(output)
    path: str = f"{root_folder}/{dag_id}/{task_id}"
    client.put_object(Bucket=bucket_name, Key=path, Body=data)
    return path


def validate_s3_path(path: str, dag_id: str, task_id: str) -> bool:
    """
    this function validates if this path exists in s3, returns a boolean value
    """
    input_path: str = f"{root_folder}/{dag_id}/{task_id}"
    if path == input_path:
        s3 = s3_client()
        try:
            s3.head_object(Bucket=bucket_name, Key=path)
            return True
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
    else:
        return False


def should_write_s3(output: Any) -> bool:
    """
    This function checks if the value provided by the client should be written to s3
    """
    return type(output) not in primitives

