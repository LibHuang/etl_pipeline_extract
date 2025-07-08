#Upload files to S3
import os
from dotenv import load_dotenv
import boto3
import json
from datetime import datetime
import requests
import time
import random

#load enviornment
load_dotenv()

#boot up s3 bucket
s3 = boto3.client('s3')

# List buckets to test
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])