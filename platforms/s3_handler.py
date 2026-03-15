import os
import logging
import boto3
import pickle
from typing import Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


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
    try:
        client = s3_client()
        response: dict = client.get_object(Key=path, Bucket=bucket_name)
        output: Any = pickle.loads(response["Body"].read())
        client.close()
        logger.info(f"Successfully read from s3 path: {path}")
        return output
    except Exception as e:
        logger.error(f"Failed to read from s3 path {path}: {e}")
        return None


def write_to_s3(output: Any, task_id: str, dag_id: str) -> str | None:
    """
    this function writes to s3 in the path of dag_id/task_id within the root path provided in the .env file,
    returns the path which she wrote to using a pickle file
    """
    try:
        client = s3_client()
        data: bytes = pickle.dumps(output)
        path: str = f"{root_folder}/{dag_id}/{task_id}"
        client.put_object(Bucket=bucket_name, Key=path, Body=data)
        logger.info(f"Successfully wrote to s3 path: {path}")
        return path
    except Exception as e:
        logger.error(f"Failed to write to s3 for dag_id={dag_id}, task_id={task_id}: {e}")
        return None


def validate_s3_path(path: str, dag_id: str, task_id: str) -> bool | None:
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
                logger.error(f"S3 path not found: {path}")
                return False
    else:
        logger.error(f"Path mismatch: expected {input_path}, got {path}")
        return False


def should_write_s3(output: Any) -> bool:
    """
    This function checks if the value provided by the client should be written to s3
    """
    return type(output) not in primitives

