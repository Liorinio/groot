import os
import boto3
from dotenv import load_dotenv

load_dotenv()
access_key = os.environ["S3_ACCESS_KEY"]
secert_key = os.environ[""]


def read_from_s3(path):
    pass


def write_to_s3(path):
    pass


def validate_s3_path(path: str) -> bool:
    pass
